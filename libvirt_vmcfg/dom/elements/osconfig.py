from enum import Enum
from typing import Optional, Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class QemuOSConfig(Element):
    unique: bool = True

    def __init__(self, arch: str, machine: str,
                 boot_dev_order: Optional[Sequence[str]] = None):
        self.arch = arch
        self.machine = machine
        if boot_dev_order is None:
            boot_dev_order = []
        self.boot_dev_order = boot_dev_order

    def attach_xml(self, root):
        os_tag = etree.SubElement(root, "os")
        type_tag = etree.SubElement(os_tag, "type", arch=self.arch,
                                    machine=self.machine)
        type_tag.text = "hvm"

        boot_tags = []
        for dev in self.boot_dev_order:
            boot_tags.append(etree.SubElement(os_tag, "boot", dev=dev))

        return [os_tag, type_tag] + boot_tags

    def __repr__(self):
        return (f"QemuOSConfig(arch={self.arch!r}, machine={self.machine!r}, "
                f"boot_dev_order={self.boot_dev_order}")
