from lxml import etree

from libvirt_vmcfg.domain import Element


class Description(Element):
    unique = True

    def __init__(self, description):
        self.description = description

    def attach_xml(self, root):
        description_tag = etree.SubElement(root, "description")
        name_tag.text = str(self.description)
        return [name_tag]

    def __repr__(self):
        return f"Description({self.description!r})"
