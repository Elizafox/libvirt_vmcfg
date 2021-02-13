from typing import List, Sequence, cast

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class Device(Element):
    def get_devices_tag(self, root: etree._Element) -> etree._Element:
        nodes = cast(List[etree._Element], root.xpath("/domain/devices"))
        if nodes:
            return nodes[0]
        else:
            return etree.SubElement(root, "devices")

    def detach_xml(self, tags: Sequence[etree._Element]) -> None:
        if not tags:
            # If there's no tags (subclass didn't add any), nothing to do.
            # Call the superclass method anyway, just in case
            super().detach_xml(tags)
            return

        # Get the root before the tags get deleted
        tree: etree._ElementTree = tags[0].getroottree()
        root = tree.getroot()

        # This should clean up our tags
        super().detach_xml(tags)

        # Clean up the device node, if we have to.
        nodes = cast(List[etree._Element], root.xpath("/domain/devices"))
        for node in nodes:
            if not list(node):
                # Spurious type warning about parent possibly being None
                # This can't happen (HOPEFULLY), so disregard it.
                # If this invariant doesn't hold true, well, we're fucked
                # anyway.
                parent = cast(etree._Element, node.getparent())
                parent.remove(node)


# Imported here to prevent circular dependency
from libvirt_vmcfg.dom.elements.devices.channel import QemuAgentChannel
from libvirt_vmcfg.dom.elements.devices.clock import (
    TimerType, TickPolicy, Offset, Basis, RTCTrack, TSCMode, Adjustment,
    Timer, TimerRTC, TimerTSC, TimerPIT, TimerHPET, TimerKVMClock,
    TimerHyperVClock, TimerARMV, Clock
)
from libvirt_vmcfg.dom.elements.devices.console import ConsolePTY
from libvirt_vmcfg.dom.elements.devices.cpu import CPU
from libvirt_vmcfg.dom.elements.devices.disk import (
    DeviceAttachment, TargetBus, Driver, DriverType, DriverCache, DriverIO,
    DriverErrorPolicy, DriverDiscard, DriverDetectZeroes, DriverOptions,
    IOTuneOptions, DiskSource, DiskSourceBlockPath, DiskSourceNetHTTP,
    DiskTarget, DiskTargetCDROM, DiskTargetDisk, DiskTargetFloppy, Tray, Disk
)
from libvirt_vmcfg.dom.elements.devices.interface import BridgedInterface
from libvirt_vmcfg.dom.elements.devices.memballoon import VirtIOMemballoon
from libvirt_vmcfg.dom.elements.devices.rng import RNGModel, RNG
from libvirt_vmcfg.dom.elements.devices.serial import VirtIOSerialController
from libvirt_vmcfg.dom.elements.devices.usb import QemuXHCIUSBController
