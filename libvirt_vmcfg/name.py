from lxml import etree

from libvirt_vmcfg import Element


class Name(Element):
    unique = True

    def __init__(self, vm_name):
        self.vm_name = vm_name

    def attach_xml(self, root):
        name_tag = etree.SubElement(root, "name")
        name_tag.text = str(self.vm_name)
        return [name_tag]
