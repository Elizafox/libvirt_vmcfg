from typing import Optional

from lxml import etree

from libvirt_vmcfg.common.util import bool_to_str
from libvirt_vmcfg.dom.elements.features import (
    FeatureBase, FeatureEmpty, FeatureBooleanState
)


class PAE(FeatureEmpty):
    name = "pae"


class NonPAE(FeatureEmpty):
    name = "nonpae"


class ACPI(FeatureEmpty):
    name = "acpi"


class APIC(FeatureBase):
    name = "apic"

    def __init__(self, eoi: Optional[bool] = None):
        self.eoi = eoi

    def xml_tag(self) -> etree._Element:
        apic_tag = etree.Element(self.name)
        if self.eoi is not None:
            apic_tag.set("eoi", bool_to_str(self.eoi))

        return apic_tag


class HAP(FeatureBooleanState):
    name = "hap"


class Viridian(FeatureEmpty):
    name = "viridian"


class PVSpinlock(FeatureBooleanState):
    name = "pvspinlock"


class PMU(FeatureBooleanState):
    name = "pmu"


class GIC(FeatureBase):
    name = "gic"

    def __init__(self, state: bool, version: Optional[int] = None):
        self.state = state
        self.version = version

    def xml_tag(self) -> etree._Element:
        if self.version is None:
            version = None
        elif self.version > 0:
            version = str(self.version)
        else:
            version = "host"

        gic_tag = etree.Element(self.name, state=bool_to_str(self.state))

        if version is not None:
            gic_tag.set("version", str(self.version))

        return gic_tag
