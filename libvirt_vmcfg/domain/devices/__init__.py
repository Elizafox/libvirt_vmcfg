from lxml import etree

from libvirt_vmcfg.domain import Element


class Device(Element):
    def get_devices_tag(self, root):
        nodes = root.xpath("/domain/devices")
        if nodes:
            return nodes[0]
        else:
            return etree.SubElement(root, "devices")

    def detach_xml(self, tags):
        root = tags[0].getroottree().getroot()
        super().detach_xml(tags)

        for node in root.xpath("/domain/devices"):
            if not node.getchildren():
                node.getparent().remove(node)
