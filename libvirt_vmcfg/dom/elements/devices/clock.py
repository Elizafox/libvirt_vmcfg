from enum import Enum
from typing import Dict, NamedTuple, Optional, Sequence

from lxml import etree

from libvirt_vmcfg.dom import Element


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


class OffsetType(Enum):
    UTC = "utc"
    LOCALTIME = "localtime"
    TIMEZONE = "timezone"
    VARIABLE = "variable"


class TimerDefinition(NamedTuple):
    type: TimerType
    tickpolicy: Optional[TickPolicy]
    present: bool
    args: Optional[Dict[str, str]]


class Clock(Element):
    unique: bool = True

    def __init__(self, offset: OffsetType = OffsetType.UTC,
                 timers: Optional[Sequence[TimerDefinition]] = None, *,
                 offset_args: Optional[Dict[str, str]] = None):
        if timers is None:
            timers = (
                TimerDefinition(TimerType.RTC, TickPolicy.CATCHUP, True, None),
                TimerDefinition(TimerType.PIT, TickPolicy.DELAY, True, None),
                TimerDefinition(TimerType.HPET, None, False, None),
            )

        self.offset = offset
        self.offset_args = offset_args
        self.timers = timers

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        clock_tag = etree.SubElement(root, "clock")
        if self.offset and self.offset.value:
            clock_tag.attrib["offset"] = self.offset.value

        if self.offset_args:
            {clock_tag.attrib[k]: v for k, v in self.offset_args.items()}

        # Attach subtags for timers
        for timer in self.timers:
            timer_tag = etree.SubElement(clock_tag, "timer",
                                         name=timer.type.value)
            if not timer.present:
                timer_tag.attrib["present"] = "no"
                continue

            if timer.tickpolicy and timer.tickpolicy.value:
                timer_tag.attrib["tickpolicy"] = timer.tickpolicy.value

            if timer.args:
                {timer_tag.attrib[k]: v for k, v in timer.args.items()}

        return [clock_tag]

    def __repr__(self):
        return f"Clock(offset={self.offset}, timers={self.timers})"
