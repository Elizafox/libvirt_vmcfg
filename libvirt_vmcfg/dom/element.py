from abc import abstractmethod, ABC
from enum import Enum
from typing import Any, List, Sequence, cast

from lxml import etree


class Element(ABC):
    """Base element class."""

    # Required attribute
    unique: bool = False

    @staticmethod
    def bool_to_str(val: bool) -> str:
        return "yes" if val else "no"

    # XXX - the arguments to etree.SubElement are too complicated to describe.
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
