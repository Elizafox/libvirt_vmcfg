from typing import Optional, Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class Memory(Element):
    unique: bool = True

    def __init__(self, memory: int, current_memory: Optional[int] = None):
        self.memory = memory
        self.current_memory: int
        if current_memory is None:
            self.current_memory = memory
        else:
            self.current_memory = current_memory

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        memory_tag = etree.SubElement(root, "memory")
        memory_tag.text = str(self.memory)

        current_memory_tag = etree.SubElement(root, "currentMemory")
        current_memory_tag.text = str(self.current_memory)

        return [memory_tag, current_memory_tag]

    def __repr__(self):
        return (f"Memory(memory={self.memory}, "
                f"current_memory={self.current_memory})")
