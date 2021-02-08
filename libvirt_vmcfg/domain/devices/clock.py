from enum import Enum
from typing import NamedTuple, Optional, Sequence

from lxml import etree

from libvirt_vmcfg.domain import Element


class TimerType(Enum):
    RTC = "rtc"
    PIT = "pit"
    HPET = "hpet"


class TickPolicy(Enum):
    UNKNOWN = ""
    CATCHUP = "catchup"
    DELAY = "delay"


class OffsetType(Enum):
    UNKNOWN = ""
    UTC = "utc"


class TimerDefinition(NamedTuple):
    type: TimerType
    tickpolicy: Optional[TickPolicy]
    present: bool


class Clock(Element):
    unique: bool = True

    def __init__(self, offset: OffsetType = OffsetType.UTC,
                 timers: Optional[Sequence[TimerDefinition]] = None):
        if timers is None:
            timers = (
                TimerDefinition(TimerType.RTC, TickPolicy.CATCHUP, True),
                TimerDefinition(TimerType.PIT, TickPolicy.DELAY, True),
                TimerDefinition(TimerType.HPET, None, False),
            )

        self.offset = offset
        self.timers = timers

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        clock_tag = etree.SubElement(root, "clock")
        if self.offset and self.offset.value:
            clock_tag.attrib["offset"] = self.offset.value

        # Attach subtags for timers
        for timer in self.timers:
            timer_tag = etree.SubElement(clock_tag, "timer",
                                         name=timer.type.value)
            if not timer.present:
                timer_tag.attrib["present"] = "no"
            elif timer.tickpolicy and timer.tickpolicy.value:
                timer_tag.attrib["tickpolicy"] = timer.tickpolicy.value

        return [clock_tag]

    def __repr__(self):
        return f"Clock(offset={self.offset}, timers={self.timers})"
