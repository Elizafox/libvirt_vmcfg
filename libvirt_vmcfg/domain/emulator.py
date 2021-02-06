from lxml import etree

from libvirt_vmcfg.domain.devices import Device


class Emulator(Device):
    unique = True

    def __init__(self, emulator_path):
        self.emulator_path = emulator_path

    def attach_xml(self, root):
        devices_tag = self.get_devices_tag(root)
        emulator_tag = etree.SubElement(devices_tag, "emulator")
        emulator_tag.text = str(self.emulator_path)
        return [emulator_tag]

    def __repr__(self):
        return f"Emulator({self.emulator_path!r})"
