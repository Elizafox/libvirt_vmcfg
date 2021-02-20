from dataclasses import astuple, dataclass, field
from enum import Enum
from typing import Optional

from lxml import etree

from libvirt_vmcfg.common.util import bool_to_str
from libvirt_vmcfg.dom.elements.features import (
    FeatureBase, FeatureEmpty, FeatureBooleanState
)


class IOAPICDriver(Enum):
    KVM = "kvm"
    QEMU = "qemu"


class HPTResizing(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    REQUIRED = "required"


class CFPCValue(Enum):
    BROKEN = "broken"
    WORKAROUND = "workaround"
    FIXED = "fixed"


class SBBCValue(Enum):
    BROKEN = "broken"
    WORKAROUND = "workaround"
    FIXED = "fixed"


class IBSValue(Enum):
    BROKEN = "broken"
    WORKAROUND = "workaround"
    FIXED = "fixed"
    FIXED_CCD = "fixed-ccd"
    FIXED_NA = "fixed-na"
    FIXED_IBS = "fixed-ibs"


class SMM(FeatureBase):
    name = "smm"

    def __init__(self, state: bool, tseg: Optional[int] = None,
                 unit: Optional[str] = "MiB"):
        self.state = state
        self.tseg = tseg
        self.unit = unit

    def xml_tag(self) -> etree._Element:
        smm_tag = etree.Element(self.name, state=bool_to_str(self.state))

        if self.tseg:
            tseg_tag = etree.SubElement(smm_tag, "tseg")
            if self.unit:
                tseg_tag.set("unit", self.unit)

            tseg_tag.text = str(self.tseg)

        return smm_tag


class IOAPIC(FeatureBase):
    name = "ioapic"

    def __init__(self, driver: IOAPICDriver):
        self.driver = driver

    def xml_tag(self) -> etree._Element:
        return etree.Element(self.name, driver=self.driver.value)


class HPT(FeatureBase):
    name = "hpt"

    def __init__(self, resizing: Optional[HPTResizing] = None,
                 maxpagesize: Optional[int] = None,
                 unit: Optional[str] = "MiB"):
        self.resizing = resizing
        self.maxpagesize = maxpagesize
        self.unit = unit

    def xml_tag(self) -> etree._Element:
        hpt_tag = etree.Element(self.name, resizing=self.resizing.value)

        if self.maxpagesize is not None:
            maxpagesize_tag = etree.SubElement(hpt_tag, "maxpagesize")
            maxpagesize_tag.text = str(self.maxpagesize)
            if self.unit is not None:
                maxpagesize_tag.set("unit", self.unit)

        return hpt_tag


class VMCoreInfo(FeatureEmpty):
    name = "vmcoreinfo"


class HTM(FeatureBooleanState):
    name = "htm"


class NestedHV(FeatureBooleanState):
    name = "nested-hv"


class CCFAssist(FeatureBooleanState):
    name = "ccf-assist"


class CFPC(FeatureBase):
    name = "cfpc"

    def __init__(self, value: CFPCValue):
        self.value = value

    def xml_tag(self) -> etree._Element:
        return etree.Element(self.name, value=self.value.value)


class SBBC(FeatureBase):
    name = "sbbc"

    def __init__(self, value: SBBCValue):
        self.value = value

    def xml_tag(self) -> etree._Element:
        return etree.Element(self.name, value=self.value.value)


class IBS(FeatureBase):
    def __init__(self, value: IBSValue):
        self.value = value

    def xml_tag(self) -> etree._Element:
        return etree.Element(self.name, value=self.value.value)


#############################
# KVM tag specific features #
#############################

class KVMHidden(FeatureBooleanState):
    name = "hidden"
    parent = "kvm"


class KVMHintDedicated(FeatureBooleanState):
    name = "hint-dedicated"
    parent = "kvm"


class KVMPollControl(FeatureBooleanState):
    name = "poll-control"
    parent = "kvm"


@dataclass
class KVMFeatureSet:
    hidden: Optional[KVMHidden] = None
    hint_dedicated: Optional[KVMHintDedicated] = None
    poll_control: Optional[KVMPollControl] = None


class KVM(FeatureBase):
    name = "kvm"

    def __init__(self, features: KVMFeatureSet):
        features_tuple = astuple(features)
        if features_tuple == (None,) * len(features_tuple):
            raise ValueError("No feature bits set")

        self.features = features

    def xml_tag(self) -> etree._Element:
        kvm_tag = etree.Element(self.name)

        for feature in astuple(self.features):
            assert feature.parent == self.name
            kvm_tag.append(feature.xml_tag())

        return kvm_tag


######################################
# HyperV-specific options (QEMU/KVM) #
######################################

class HyperVRelaxed(FeatureBooleanState):
    name = "relaxed"
    parent = "hyperv"


class HyperV_VAPIC(FeatureBooleanState):
    name = "vapic"
    parent = "hyperv"


class HyperVSpinlocks(FeatureBase):
    name = "spinlocks"
    parent = "hyperv"

    def __init__(self, state: bool, retries: Optional[int] = None):
        if retries is not None and retries < 4095:
            raise ValueError("retries must be at least 4095", retries)

        self.state = state
        self.retries = retries

    def xml_tag(self) -> etree._Element:
        spinlocks_tag = etree.Element(self.name, state=bool_to_str(self.state))

        if self.retries is not None:
            spinlocks_tag.set("retries", str(self.retries))

        return spinlocks_tag


class HyperV_VPIndex(FeatureBooleanState):
    name = "vpindex"
    parent = "hyperv"


class HyperVRuntime(FeatureBooleanState):
    name = "runtime"
    parent = "hyperv"


class HyperVSynIC(FeatureBooleanState):
    name = "synic"
    parent = "hyperv"


class HyperVStimer(FeatureBase):
    name = "stimer"
    parent = "hyperv"

    def __init__(self, state: bool, direct: Optional[bool] = None):
        self.state = state
        self.direct = direct

    def xml_tag(self) -> etree._Element:
        stimer_tag = etree.Element(self.name, state=bool_to_str(self.state))

        if self.direct is not None:
            etree.SubElement(stimer_tag, "direct",
                             state=bool_to_str(self.state))

        return stimer_tag


class HyperVReset(FeatureBooleanState):
    name = "reset"
    parent = "hyperv"


class HyperV_VendorID(FeatureBase):
    name = "vendor_id"
    parent = "hyperv"

    def __init__(self, state: bool, value: Optional[str] = None):
        if value is not None and len(value) > 12:
            raise ValueError("value must be 12 characters or less", value)

        self.state = state
        self.value = value

    def xml_tag(self) -> etree._Element:
        vendor_id_tag = etree.Element(self.name, state=bool_to_str(self.state))

        if self.value is not None:
            vendor_id_tag.set("value", self.value)

        return vendor_id_tag


class HyperVFrequencies(FeatureBooleanState):
    name = "frequencies"
    parent = "hyperv"


class HyperVReenlightenment(FeatureBooleanState):
    name = "reenlightenment"
    parent = "hyperv"


class HyperVTLBFlush(FeatureBooleanState):
    name = "tlbflush"
    parent = "hyperv"


class HyperVIPI(FeatureBooleanState):
    name = "ipi"
    parent = "hyperv"


class HyperVEVMCS(FeatureBooleanState):
    name = "evmcs"
    parent = "hyperv"


@dataclass
class HyperVFeatureSet:
    # NB: lambda is used to create factories for these objects.
    relaxed: Optional[HyperVRelaxed] = \
        field(default_factory=lambda: HyperVRelaxed(True))
    vapic : Optional[HyperV_VAPIC] = \
        field(default_factory=lambda: HyperV_VAPIC(True))
    spinlocks : Optional[HyperVSpinlocks] = \
        field(default_factory=lambda: HyperVSpinlocks(True, 4096))
    vpindex: Optional[HyperV_VPIndex] = \
        field(default_factory=lambda: HyperV_VPIndex(True))
    runtime: Optional[HyperVRuntime] = \
        field(default_factory=lambda: HyperVRuntime(True))
    synic: Optional[HyperVSynIC] = \
        field(default_factory=lambda: HyperVSynIC(True))
    stimer: Optional[HyperVStimer] = \
        field(default_factory=lambda: HyperVStimer(True, True))
    reset: Optional[HyperVReset] = \
        field(default_factory=lambda: HyperVReset(True))
    vendor_id: Optional[HyperV_VendorID] = \
        field(default_factory=lambda: HyperV_VendorID(True))
    frequencies: Optional[HyperVFrequencies] = \
        field(default_factory=lambda: HyperVFrequencies(True))
    reenlightenment: Optional[HyperVReenlightenment] = \
        field(default_factory=lambda: HyperVReenlightenment(True))
    tlbflush: Optional[HyperVTLBFlush] = \
        field(default_factory=lambda: HyperVTLBFlush(True))
    ipi: Optional[HyperVIPI] = \
        field(default_factory=lambda: HyperVIPI(True))
    evmcs: Optional[HyperVEVMCS] = \
        field(default_factory=lambda: HyperVEVMCS(True))


class HyperV(FeatureBase):
    name = "hyperv"

    def __init__(self, features: HyperVFeatureSet):
        features_tuple = astuple(features)
        if features_tuple == (None,) * len(features_tuple):
            raise ValueError("No feature bits set")

        self.features = features

    def xml_tag(self) -> etree._Element:
        hyperv_tag = etree.Element(self.name)

        for feature in astuple(self.features):
            assert feature.parent == self.name
            hyperv_tag.append(feature.xml_tag())

        return hyperv_tag
