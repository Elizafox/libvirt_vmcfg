from lxml import etree

from libvirt_vmcfg.domain import Element


class FeaturesSimple(Element):
    unique = True

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def attach_xml(self, root):
        if not self.kwargs:
            return

        features_tag = etree.SubElement(root, "features")
        for key, value in self.kwargs.items():
            if not value:
                continue

            tag = etree.SubElement(features_tag, key)
    
    def __repr__(self):
        return f"FeaturesSimple(kwargs={self.kwargs})"
 

class X86Features(FeaturesSimple):
    unique = True

    def __init__(self, acpi=True, apic=True):
        super().__init__(acpi=acpi, apic=apic)

    def __repr__(self):
        acpi = self.kwargs["acpi"]
        apic = self.kwargs["apic"]
        return f"X86Features(acpi={acpi}, apic={apic})"
