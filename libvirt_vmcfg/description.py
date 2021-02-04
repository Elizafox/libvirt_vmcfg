from lxml import etree

from libvirt_vmcfg import Element


class Description(Element):
    unique = True

    def __init__(self, description):
        self.description = description

    def attach_xml(self, root):
        description_tag = etree.SubElement(root, "description")
        name_tag.text = str(self.description)
        return [name_tag]
