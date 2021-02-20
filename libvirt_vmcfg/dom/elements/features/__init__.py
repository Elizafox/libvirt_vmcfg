from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union

from lxml import etree

from libvirt_vmcfg.common.util import bool_to_str
from libvirt_vmcfg.dom.elements import Element


class FeatureBase(ABC):
    parent: Optional[Union[FeatureBase, str]] = None
    name: str

    @abstractmethod
    def xml_tag(self) -> etree._Element:
        raise NotImplementedError


class FeatureEmpty(FeatureBase):
    def xml_tag(self) -> etree._Element:
        return etree.Element(self.name)


class FeatureBooleanState(FeatureBase): 
    def __init__(self, state: bool):
        self.state = state

    def xml_tag(self) -> etree._Element:
        return etree.Element(self.name, state=bool_to_str(self.state))


class Features(Element):
    unique = True

    def __init__(self, features: Sequence[FeatureBase]):
        for feature in features:
            if feature.parent is not None:
                raise ValueError(f"Feature not for standalone use "
                                 f"(requires parent {feature.parent})",
                                 feature.name, feature.parent)

        self.features = features

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        features_tag = etree.SubElement(root, "features")
        for feature in self.features:
            features_tag.append(feature.xml_tag())

        return [features_tag]


# Delayed import to prevent circular deps
from libvirt_vmcfg.dom.elements.features.common import (
    PAE, NonPAE, ACPI, APIC, HAP, Viridian, PVSpinlock, PMU, GIC
)
from libvirt_vmcfg.dom.elements.features.kvm import (
    IOAPICDriver, HPTResizing, CFPCValue, SBBCValue, IBSValue, SMM, IOAPIC,
    HPT, VMCoreInfo, HTM, NestedHV, CCFAssist, CFPC, SBBC, IBS, KVMHidden,
    KVMHintDedicated, KVMPollControl, KVMFeatureSet, KVM, HyperVRelaxed,
    HyperV_VAPIC, HyperVSpinlocks, HyperV_VPIndex, HyperVRuntime, HyperVStimer,
    HyperVReset, HyperV_VendorID, HyperVFrequencies, HyperVReenlightenment,
    HyperVTLBFlush, HyperVIPI, HyperVEVMCS, HyperVFeatureSet, HyperV
)
