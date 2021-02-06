from lxml import etree

from libvirt_vmcfg.domain import Element


class Metadata(Element):
    unique = True

    def __init__(self, metadata):
        try:
            # Crude test to see if this is a node
            metadata.getroottree()
            self.metadata_root = metadata
        except AttributeError:
            try:
                # Maybe this is a tree already?
                self.metadata_root = metadata.getroot()
            except Exception as e:
                raise ValueError("Error getting metadata root") from e

    def attach_xml(self, root):
        root.append(self.metadata_root)
        return [self.metadata_root]

    def __repr__(self):
        return f"Metadata(metadata_root={self.metadata_root})"
