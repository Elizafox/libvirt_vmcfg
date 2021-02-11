from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence, Union

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class DomainType(Enum):
    UNKNOWN = ""
    KVM = "kvm"


# This is an implementation detail and should otherwise be ignored
@dataclass
class ElementData:
    tags: Sequence[etree._Element]
    element: Element


class Domain:
    """Root class for libvirt config"""
    def __init__(self, type: DomainType = DomainType.KVM,
                 elements: Optional[Sequence[Element]] = None):
        self.type: DomainType = type
        self.root: etree._Element = etree.Element("domain", type=type.value)
        self.elements: List[ElementData] = []

        if elements:
            for element in elements:
                self.attach_element(element)

    def attach_element(self, element: Element) -> ElementData:
        if element.unique:
            if any(e for e in self.elements if type(e) is type(element)):
                raise ValueError("Element already attached", element)

        tags: Sequence[etree._Element] = element.attach_xml(self.root)
        data = ElementData(tags, element)
        self.elements.append(data)
        return data

    def detach_element(self, data: ElementData) -> None:
        data.element.detach_xml(data.tags)
        self.elements.remove(data)

    def emit_xml(self, *, pretty_print: bool = False,
                 encoding: str = "unicode") -> Union[str, bytes]:
        return etree.tostring(self.root, pretty_print=pretty_print,
                              encoding=encoding)

    def __repr__(self):
        return (f"Domain(type={self.type}, root={self.root}, "
                f"elements={self.elements})")
