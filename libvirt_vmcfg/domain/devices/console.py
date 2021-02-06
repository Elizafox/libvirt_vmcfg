from lxml import etree

from libvirt_vmcfg.domain.devices import Device


class ConsolePTY(Device):
    def attach_xml(self, root):
        devices_tag = self.get_devices_tag(root)
        return [etree.SubElement(devices_tag, "console", type="pty")]

    def __repr__(self):
        return f"ConsolePTY()"
