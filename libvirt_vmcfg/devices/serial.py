from lxml import etree

from libvirt_vmcfg.devices import Device


class VirtIOSerialController(Device):
    def attach_xml(self, root):
        devices_tag = self.get_devices_tag(root)
        return [etree.SubElement(devices_tag, "controller",
                                 type="virtio-serial")]

    def __repr__(self):
        return f"VirtIOSerialController()"
