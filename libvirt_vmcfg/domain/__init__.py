from abc import abstractmethod, ABC
from enum import Enum
from typing import Any, List, NamedTuple, Optional, Sequence, Union, cast

from lxml import etree


class ElementData(NamedTuple):
    tags: Sequence[etree._Element]
    element: "Element"


class DomainType(Enum):
    UNKNOWN = ""
    KVM = "kvm"


class Domain:
    """Root class for libvirt config"""
    def __init__(self, type: DomainType = DomainType.KVM,
                 elements: Optional[Sequence["Element"]] = None):
        self.type: DomainType = type
        self.root: etree._Element = etree.Element("domain", type=type.value)
        self.elements: List[ElementData] = []

        if elements:
            for element in elements:
                self.attach_element(element)

    def attach_element(self, element: "Element") -> ElementData:
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


class Element(ABC):
    """Base element class."""

    # Required attribute
    unique: bool = False

    @staticmethod
    def bool_to_str(val: bool) -> str:
        return "yes" if val else "no"

    def node_find_or_create(self, _root: etree._Element, _name: str,
                            **kwargs: Any) -> etree._Element:
        nodelist = cast(List[etree._Element], _root.xpath(f"/domain/{_name}"))
        if nodelist:
            return nodelist[0]
        else:
            return etree.SubElement(_root, _name, **kwargs)

    @abstractmethod
    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        raise NotImplementedError

    def detach_xml(self, tags: Sequence[etree._Element]) -> None:
        for tag in tags:
            parent = cast(etree._Element, tag.getparent())
            parent.remove(tag)
