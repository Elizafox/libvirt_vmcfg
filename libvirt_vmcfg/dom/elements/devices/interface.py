from os import urandom
from typing import Optional, Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements.devices import Device


def gen_mac() -> str:
    seq = list(urandom(6))
    # Clear group bit and set local only bit
    seq[0] &= ~0x1
    seq[0] |= 0x2
    return ":".join(f"{octet:0{2}x}" for octet in seq)


class BridgedInterface(Device):
    unique: bool = False

    def __init__(self, interface: str, mac: Optional[str] = None,
                 model: str = "virtio"):
        self.interface = interface
        self.mac = gen_mac() if mac is None else mac
        self.model = model

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
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
