from typing import List, Sequence, cast

from lxml import etree

from libvirt_vmcfg.domain import Element


class Device(Element):
    def get_devices_tag(self, root: etree._Element) -> etree._Element:
        nodes = cast(List[etree._Element], root.xpath("/domain/devices"))
        if nodes:
            return nodes[0]
        else:
            return etree.SubElement(root, "devices")

    def detach_xml(self, tags: Sequence[etree._Element]) -> None:
        if not tags:
            # If there's no tags (subclass didn't add any), nothing to do.
            # Call the superclass method anyway, just in case
            super().detach_xml(tags)
            return

        # Get the root before the tags get deleted
        tree: etree._ElementTree = tags[0].getroottree()
        root = tree.getroot()
        super().detach_xml(tags)

        # Now search for the correct node
        nodes = cast(List[etree._Element], root.xpath("/domain/devices"))
        for node in nodes:
            if not list(node):
                # Spurious type warning about parent possibly being None
                # This can't happen so disregard it.
                parent = cast(etree._Element, node.getparent())
                parent.remove(node)
