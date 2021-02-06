from enum import Enum

from lxml import etree

from libvirt_vmcfg.domain import Element


class VirtTypes(Enum):
    HVM = "hvm"


class OSConfig(Element):
    unique = True

    def __init__(self, arch, machine, type=VirtTypes.HVM, boot_dev_order=None):
        self.arch = arch
        self.machine = machine
        self.type = type
        if boot_dev_order is None:
            boot_dev_order = []
        self.boot_dev_order = boot_dev_order

    def attach_xml(self, root):
        os_tag = etree.SubElement(root, "os")
        type_tag = etree.SubElement(os_tag, "type", arch=self.arch,
                                    machine=self.machine)
        type_tag.text = self.type.value

        boot_tags = []
        for dev in self.boot_dev_order:
            boot_tags.append(etree.SubElement(os_tag, "boot", dev=dev))

        return [os_tag, type_tag] + boot_tags

    def __repr__(self):
        return (f"OSConfig(arch={self.arch!r}, machine={self.machine!r}, "
                f"type={self.type}, boot_dev_order={self.boot_dev_order}")


class QemuOSConfig(OSConfig):
    unique = True

    def __init__(self, arch, machine, boot_dev_order=None):
        # HVM is the only option on QEMU/KVM
        super().__init__(arch, machine, VirtTypes.HVM, boot_dev_order)

    def __repr__(self):
        return (f"QemuOSConfig(arch={self.arch!r}, machine={self.machine!r}, "
                f"boot_dev_order={self.boot_dev_order}")
