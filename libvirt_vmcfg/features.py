from lxml import etree

from libvirt_vmcfg import Element


class Features(Element):
    unique = True

    def __init__(self, acpi=True, apic=True):
        self.acpi = acpi
        self.apic = apic

    def attach_xml(self, root):
        if not (self.acpi and self.apic):
            return

        features_tag = etree.SubElement(root, "features")
        if self.acpi:
            etree.SubElement(features_tag, "acpi")

        if self.apic:
            etree.SubElement(features_tag, "apic")

    def __repr__(self):
        return f"Features(acpi={self.acpi}, apic={self.apic})"
