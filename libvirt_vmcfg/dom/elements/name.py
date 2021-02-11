from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class Name(Element):
    unique: bool = True

    def __init__(self, name: str):
        self.name = name

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        name_tag = etree.SubElement(root, "name")
        name_tag.text = str(self.name)
        return [name_tag]

    def __repr__(self):
        return f"Name({self.name!r})"
