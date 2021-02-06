from lxml import etree

from libvirt_vmcfg.domain import Element


class CPU(Element):
    unique = True

    def __init__(self, vcpus, mode="host-model"):
        self.vcpus = vcpus
        self.mode = mode

    def attach_xml(self, root):
        vcpu_tag = etree.SubElement(root, "vcpu")
        vcpu_tag.text = str(self.vcpus)
        cpu_tag = etree.SubElement(root, "cpu", mode=self.mode)

        return [vcpu_tag, cpu_tag]

    def __repr__(self):
        return f"CPU(vcpus={self.vcpus}, mode={self.mode})"
