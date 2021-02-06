from lxml import etree

from libvirt_vmcfg.domain import Element


class Memory(Element):
    unique = True

    def __init__(self, memory, current_memory=None):
        self.memory = memory
        if current_memory is None:
            self.current_memory = memory
        else:
            self.current_memory = current_memory

    def attach_xml(self, root):
        memory_tag = etree.SubElement(root, "memory")
        memory_tag.text = str(self.memory)

        current_memory_tag = etree.SubElement(root, "currentMemory")
        current_memory_tag.text = str(self.current_memory)

        return [memory_tag, current_memory_tag]

    def __repr__(self):
        return (f"Memory(memory={self.memory}, "
                f"current_memory={self.current_memory})")
