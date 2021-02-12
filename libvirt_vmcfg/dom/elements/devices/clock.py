from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, NewType, Optional, Sequence, Tuple, Union

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class TimerType(Enum):
    RTC = "rtc"
    PIT = "pit"
    HPET = "hpet"
    KVMCLOCK = "kvmclock"
    TSC = "tsc"
    HYPERVCLOCK = "hypervclock"
    ARMVTIMER = "armvtimer"


class TickPolicy(Enum):
    CATCHUP = "catchup"
    DELAY = "delay"
    MERGE = "merge"
    DISCARD = "discard"


class Offset(Enum):
    UTC = "utc"
    LOCALTIME = "localtime"
    TIMEZONE = "timezone"
    VARIABLE = "variable"


class Basis(Enum):
    """Used in clocks with a variable offset."""
    UTC = "utc"
    LOCALTIME = "localtime"


class RTCTrack(Enum):
    """Only valid for RTC timers."""
    BOOT = "boot"
    GUEST = "guest"
    WALL = "wall"
    REALTIME = "realtime"


class TSCMode(Enum):
    """Only valid for TSC timers."""
    AUTO = "auto"
    NATIVE = "native"
    EMULATE = "emulate"
    PARAVIRT = "paravirt"
    SMPSAFE = "smpsafe"


class Adjustment(Enum):
    """Used for non-integer adjustments."""
    RESET = "reset"


class Timer(ABC):
    """
    The base timer interface.
    """
    type: TimerType

    def __init__(self, present: bool = True,
                 tickpolicy: Optional[TickPolicy] = None,
                 threshold: Optional[int] = None, slew: Optional[int] = None,
                 limit: Optional[int] = None):
        # Implement the lowest common denominator options.
        self.present = present
        self.tickpolicy = tickpolicy
        self.threshold = threshold
        self.slew = slew
        self.limit = limit

    def setup_timer_common(self, clock_tag: etree._Element) \
            -> Tuple[etree._Element, bool]:
        # Common bits for the timer setup
        # Factored into here as attach_xml is part of the interface
        # Returns a tuple with the tag and whether or not to proceed.
        timer_tag = etree.SubElement(clock_tag, "timer", name=self.type.value)
        if not self.present:
            timer_tag.attrib["present"] = "no"
            return (timer_tag, False)

        if self.tickpolicy is not None:
            timer_tag.attrib["tickpolicy"] = self.tickpolicy.value

        if self.tickpolicy is not TickPolicy.CATCHUP:
            # Initalisation completed
            return (timer_tag, True)

        if (self.threshold, self.slew, self.limit) == (None, None, None):
            # Nothing to do
            return (timer_tag, True)

        catchup_tag = etree.SubElement(timer_tag, "catchup")
        if self.threshold is not None:
            catchup_tag.attrib["threshold"] = str(self.threshold)

        if self.slew is not None:
            catchup_tag.attrib["slew"] = str(self.slew)

        if self.limit is not None:
            catchup_tag.attrib["limit"] = str(self.limit)

        return (timer_tag, True)

    @abstractmethod
    def attach_xml(self, clock_tag: etree._Element) -> None:
        raise NotImplementedError


class _NormalTimer(Timer):
    # A largely sufficient class for implementing most timers.
    def attach_xml(self, clock_tag: etree._Element) -> None:
        self.setup_timer_common(clock_tag)


class TimerRTC(Timer):
    type: TimerType = TimerType.RTC

    def __init__(self, *, present: bool = True,
                 tickpolicy: Optional[TickPolicy] = None,
                 threshold: Optional[int] = None, slew: Optional[int] = None,
                 limit: Optional[int] = None,
                 track: Optional[RTCTrack] = None):
        super().__init__(present, tickpolicy, threshold, slew, limit)
        self.track = track

    def attach_xml(self, clock_tag: etree._Element) -> None:
        timer_tag, proceed = self.setup_timer_common(clock_tag)
        if not proceed:
            return

        if self.track:
            timer_tag.attrib["track"] = self.track.value


class TimerTSC(Timer):
    type: TimerType = TimerType.TSC

    def __init__(self, *, present: bool = True,
                 tickpolicy: Optional[TickPolicy] = None,
                 threshold: Optional[int] = None, slew: Optional[int] = None,
                 limit: Optional[int] = None,
                 mode: Optional[TSCMode] = None,
                 frequency: Optional[int] = None):
        super().__init__(present, tickpolicy, threshold, slew, limit)
        self.mode = mode
        self.frequency = frequency

    def attach_xml(self, clock_tag: etree._Element) -> None:
        timer_tag, proceed = self.setup_timer_common(clock_tag)
        if not proceed:
            return

        if self.frequency is not None:
            timer_tag.attrib["frequency"] = str(self.frequency)

        if self.mode is not None:
            timer_tag.attrib["mode"] = self.mode.value


class TimerPIT(_NormalTimer):
    type: TimerType = TimerType.PIT


class TimerHPET(_NormalTimer):
    type: TimerType = TimerType.HPET


class TimerKVMClock(_NormalTimer):
    type: TimerType = TimerType.KVMCLOCK


class TimerHyperVClock(_NormalTimer):
    type: TimerType = TimerType.HYPERVCLOCK


class TimerARMV(_NormalTimer):
    type: TimerType = TimerType.ARMVTIMER


class Clock(Element):
    unique: bool = True

    def __init__(self, *, offset: Optional[Offset] = None,
                 timezone: Optional[str] = None,
                 adjustment: Union[int, None, Adjustment] = None,
                 basis: Optional[Basis] = None,
                 timers: Optional[Sequence[Timer]] = None):
        if timers is None:
            timers = (
                TimerRTC(tickpolicy=TickPolicy.CATCHUP),
                TimerPIT(tickpolicy=TickPolicy.DELAY),
                TimerHPET(present=False),
            )

        # Do sanity checking of the arguments
        # Based on libvirt documentation 11 Feb 2021

        if adjustment is not None:
            # The adjustment parameter is a bit strange.
            # It's always optional, except with timezone, where it's invalid.
            # But, it can only be an integer for variable.
            # Don't ask me why, I don't know.
            if offset == Offset.TIMEZONE:
                raise ValueError("adjustment is not valid with timezone "
                                 "offsets", adjustment, offset)
            elif offset == Offset.VARIABLE:
                if not isinstance(adjustment, int):
                    raise ValueError("adjustment must be either None or an "
                                     "integer with variable offsets",
                                     adjustment, offset)

        if basis is not None and offset != Offset.VARIABLE:
            # basis parameter is optional for variable offsets
            raise ValueError("basis is not valid for any offset type "
                             "except variable", basis, offset)

        if timezone is None and offset == Offset.TIMEZONE:
            # timezone has to be specified for timezone offsets...
            raise ValueError("timezone is required for timezone offsets",
                             timezone, offset)
        elif timezone is not None and offset != Offset.TIMEZONE:
            # ... but otherwise isn't allowed
            raise ValueError("timezone is only valid for timezone offsets",
                             timezone, offset)

        self.offset = offset
        self.timezone = timezone
        self.adjustment = adjustment
        self.basis = basis
        self.timers = timers

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        clock_tag = etree.SubElement(root, "clock")
        if self.offset is not None:
            # Set up offset parameters
            clock_tag.attrib["offset"] = self.offset.value

            if self.adjustment is not None:
                if isinstance(self.adjustment, int):
                    clock_tag.attrib["adjustment"] = str(self.adjustment)
                else:
                    clock_tag.attrib["adjustment"] = self.adjustment.value

            if self.timezone is not None:
                clock_tag.attrib["timezone"] = self.timezone

            if self.basis is not None:
                clock_tag.attrib["basis"] = self.basis.value

        # Attach subtags for timers
        for timer in self.timers:
            timer.attach_xml(clock_tag)

        return [clock_tag]

    def __repr__(self):
        return f"Clock(offset={self.offset}, timers={self.timers})"
