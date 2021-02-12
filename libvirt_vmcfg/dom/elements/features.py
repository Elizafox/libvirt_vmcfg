from typing import Optional, Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class FeaturesSimple(Element):
    unique: bool = True

    def __init__(self, **kwargs: Optional[bool]):
        self.kwargs = kwargs

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        if not self.kwargs:
            return []

        features_tag = etree.SubElement(root, "features")
        for key, value in self.kwargs.items():
            if not value:
                continue

            tag = etree.SubElement(features_tag, key)

        return [features_tag]

    def __repr__(self):
        return f"FeaturesSimple(kwargs={self.kwargs})"


class X86Features(FeaturesSimple):
    unique: bool = True

    def __init__(self, acpi: bool = True, apic: bool = True):
        super().__init__(acpi=acpi, apic=apic)

    def __repr__(self):
        acpi = self.kwargs["acpi"]
        apic = self.kwargs["apic"]
        return f"X86Features(acpi={acpi}, apic={apic})"
