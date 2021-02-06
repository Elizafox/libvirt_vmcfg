from collections.abc import Sequence

from lxml import etree

from libvirt_vmcfg.domain.devices import Device


class QemuXHCIUSBController(Device):
    def __init__(self, ports: int = 15):
        self.ports = ports

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        devices_tag = self.get_devices_tag(root)
        return [etree.SubElement(devices_tag, "controller", type="usb",
                                 model="qemu-xhci", ports=str(self.ports))]

    def __repr__(self):
        return f"QemuXHCIUSBController(ports={self.ports})"
