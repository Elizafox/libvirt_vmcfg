from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements.devices import Device


class VirtIOSerialController(Device):
    unique: bool = False

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        devices_tag = self.get_devices_tag(root)
        return [etree.SubElement(devices_tag, "controller",
                                 type="virtio-serial")]

    def __repr__(self):
        return f"VirtIOSerialController()"
