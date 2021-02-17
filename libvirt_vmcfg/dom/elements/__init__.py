from abc import abstractmethod, ABC
from enum import Enum
from typing import Any, List, Sequence, cast

from lxml import etree


class Element(ABC):
    """Base element class."""

    # Required attribute
    unique: bool = False

    # XXX - the arguments to etree.SubElement are too complicated to describe.
    def node_find_or_create(self, _root: etree._Element, _name: str,
                            **kwargs: Any) -> etree._Element:
        nodelist = cast(List[etree._Element], _root.xpath(f"/domain/{_name}"))
        if nodelist:
            return nodelist[0]
        else:
            return etree.SubElement(_root, _name, **kwargs)

    @abstractmethod
    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        raise NotImplementedError

    def detach_xml(self, tags: Sequence[etree._Element]) -> None:
        for tag in tags:
            parent = cast(etree._Element, tag.getparent())
            parent.remove(tag)


# Exported implementation
from libvirt_vmcfg.dom.elements.description import Description
from libvirt_vmcfg.dom.elements.emulator import Emulator
from libvirt_vmcfg.dom.elements.features import (
    FeatureBase, FeatureEmpty, FeatureBooleanState, Features, PAE, NonPAE,
    ACPI, APIC, HAP, Viridian, PVSpinlock, PMU, GIC, IOAPICDriver, HPTResizing,
    CFPCValue, SBBCValue, IBSValue, SMM, IOAPIC, HPT, VMCoreInfo, HTM,
    NestedHV, CCFAssist, CFPC, SBBC, IBS, KVMHidden, KVMHintDedicated,
    KVMPollControl, KVMFeatureSet, KVM, HyperVRelaxed, HyperV_VAPIC,
    HyperVSpinlocks, HyperV_VPIndex, HyperVRuntime, HyperVStimer, HyperVReset,
    HyperV_VendorID, HyperVFrequencies, HyperVReenlightenment, HyperVTLBFlush,
    HyperVIPI, HyperVEVMCS, HyperVFeatureSet, HyperV
)
from libvirt_vmcfg.dom.elements.memory import Memory
from libvirt_vmcfg.dom.elements.metadata import Metadata
from libvirt_vmcfg.dom.elements.name import Name
from libvirt_vmcfg.dom.elements.osconfig import QemuOSConfig
from libvirt_vmcfg.dom.elements.power_management import PowerManagement
from libvirt_vmcfg.dom.elements.uuid import DomainUUID
