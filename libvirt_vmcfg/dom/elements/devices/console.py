from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements.devices import Device


class ConsolePTY(Device):
    unique: bool = True

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        devices_tag = self.get_devices_tag(root)
        return [etree.SubElement(devices_tag, "console", type="pty")]

    def __repr__(self):
        return f"ConsolePTY()"
