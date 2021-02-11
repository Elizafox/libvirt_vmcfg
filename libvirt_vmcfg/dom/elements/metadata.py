from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class Metadata(Element):
    unique: bool = True

    def __init__(self, metadata: etree._Element):
        self.metadata = metadata

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        root.append(self.metadata)
        return [self.metadata]

    def __repr__(self):
        return f"Metadata(metadata={self.metadata})"
