from typing import Sequence

from lxml import etree

from libvirt_vmcfg.domain import Element


class Name(Element):
    unique: bool = True

    def __init__(self, vm_name: str):
        self.vm_name = vm_name

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        name_tag = etree.SubElement(root, "name")
        name_tag.text = str(self.vm_name)
        return [name_tag]

    def __repr__(self):
        return f"Name({self.vm_name!r})"
