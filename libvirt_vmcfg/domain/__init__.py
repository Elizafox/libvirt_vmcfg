from collections import namedtuple
from enum import Enum

from abc import abstractmethod, ABC

from lxml import etree


ElementData = namedtuple("ElementData", "tags element")


class DomainType(Enum):
    UNKNOWN = ""
    KVM = "kvm"


class Domain:
    """Root class for libvirt config"""
    def __init__(self, type=DomainType.KVM, elements=None):
        self.type = type
        self.root = etree.Element("domain", type=type.value)
        self.elements = []

        if elements:
            for element in elements:
                self.attach_element(element)

    def attach_element(self, element):
        if element.unique:
            # Attempt to find element
            for element2 in self.elements:
                if (isinstance(element2, element.__class__)
                    and element.name == element2.name):
                    raise ValueError("Element already attached", element)

        tags = element.attach_xml(self.root)
        self.elements.append(ElementData(tags, element))

    def detach_element(self, element):
        data = None
        for data2 in self.elements:
            if element == data2.element:
                data = data2
                break

        if data is None:
            raise ValueError("element not found", element)

        element.detach_xml(data.tags)
        self.elements.remove(data)

    def emit_xml(self, *, pretty_print=False, encoding="unicode"):
        return etree.tostring(self.root, pretty_print=pretty_print,
                              encoding=encoding)

    def __repr__(self):
        return (f"Domain(type={self.type}, root={self.root}, "
                f"elements={self.elements})")


class Element(ABC):
    """Base element class."""

    # Required attribute
    unique = False

    @property
    def name(self):
        return self.__class__.__name__

    @staticmethod
    def bool_to_str(val):
        return "yes" if val else "no"

    def element_find_or_create(self, _root, _name, **kwargs):
        nodelist = _root.xpath(f"/domain/{_name}")
        if nodelist:
            return nodelist[0]
        else:
            return etree.SubElement(_root, _name, **kwargs)

    @abstractmethod
    def attach_xml(self, root):
        raise NotImplementedError

    def detach_xml(self, tags):
        for tag in tags:
            tag.getparent().remove(tag)
