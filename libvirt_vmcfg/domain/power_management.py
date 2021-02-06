from lxml import etree

from libvirt_vmcfg.domain import Element


class PowerManagement(Element):
    unique = True

    def __init__(self, suspend_to_mem=False, suspend_to_disk=False):
        self.suspend_to_mem = suspend_to_mem
        self.suspend_to_disk = suspend_to_disk

    def attach_xml(self, root):
        pm_tag = etree.SubElement(root, "pm")
        etree.SubElement(pm_tag, "suspend-to-mem",
                         enabled=self.bool_to_str(self.suspend_to_mem))
        etree.SubElement(pm_tag, "suspend-to-disk",
                         enabled=self.bool_to_str(self.suspend_to_disk))
        return [pm_tag]

    def __repr__(self):
        return (f"PowerManagement(suspend_to_mem={self.suspend_to_mem}, "
                f"suspend_to_disk={self.suspend_to_disk})")
