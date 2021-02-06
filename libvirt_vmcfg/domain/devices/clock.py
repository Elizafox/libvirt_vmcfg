from enum import Enum
from collections import namedtuple

from lxml import etree

from libvirt_vmcfg.domain import Element


class TickPolicy(Enum):
    UNKNOWN = ""
    CATCHUP = "catchup"
    DELAY = "delay"


class OffsetType(Enum):
    UNKNOWN = ""
    UTC = "utc"


class TimerType(Enum):
    RTC = "rtc"
    PIT = "pit"
    HPET = "hpet"


TimerDefinition = namedtuple("TimerDefinition", "type tickpolicy present")


class Clock(Element):
    unique = True

    def __init__(self, offset=OffsetType.UTC, timers=None):
        if timers is None:
            timers = (
                TimerDefinition(TimerType.RTC, TickPolicy.CATCHUP, True),
                TimerDefinition(TimerType.PIT, TickPolicy.DELAY, True),
                TimerDefinition(TimerType.HPET, None, False),
            )

        self.offset = offset
        self.timers = timers

    def attach_xml(self, root):
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
