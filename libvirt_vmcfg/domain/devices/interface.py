from os import urandom

from lxml import etree

from libvirt_vmcfg.domain.devices import Device


class BridgedInterface(Device):
    unique = False

    def __init__(self, interface, mac=None, model="virtio"):
        self.interface = interface
        self.mac = self.gen_mac() if mac is None else mac
        self.model = model

    @staticmethod
    def gen_mac():
        seq = list(urandom(6))
        # Clear group bit and set local only bit
        seq[0] &= ~0x1
        seq[0] |= 0x2
        return ":".join(f"{octet:0{2}x}" for octet in seq)

    def attach_xml(self, root):
        devices_tag = self.get_devices_tag(root)
        interface_tag = etree.SubElement(devices_tag, "interface",
                                         type="bridge")
        etree.SubElement(interface_tag, "source", bridge=self.interface)
        etree.SubElement(interface_tag, "mac", address=self.mac)
        etree.SubElement(interface_tag, "model", type=self.model)

        return [interface_tag]

    def __repr__(self):
        return (f"BridgedInterface(interface={self.interface!r}, "
                f"mac={self.mac!r}, model={self.model!r})")
