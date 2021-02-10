from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements.devices import Device


class QemuAgentChannel(Device):
    unique: bool = True

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        devices_tag = self.get_devices_tag(root)
        channel_tag = etree.SubElement(devices_tag, "channel", type="unix")
        source_tag = etree.SubElement(channel_tag, "source", mode="bind")
        target_tag = etree.SubElement(channel_tag, "target", type="virtio",
                                      name="org.qemu.guest_agent.0")
        return [channel_tag, source_tag, target_tag]

    def __repr__(self):
        return f"QemuAgentChannel()"
