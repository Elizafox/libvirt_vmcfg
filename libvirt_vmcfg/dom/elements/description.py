from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class Description(Element):
    unique: bool = True

    def __init__(self, description: str):
        self.description = description

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        description_tag = etree.SubElement(root, "description")
        description_tag.text = str(self.description)
        return [description_tag]

    def __repr__(self):
        return f"Description({self.description!r})"
