from collections.abc import Sequence
from typing import List, Optional, Union
from uuid import UUID, uuid4
from warnings import warn

from lxml import etree

from libvirt_vmcfg.dom import Domain, Element

from libvirt_vmcfg.dom.elements import Emulator
from libvirt_vmcfg.dom.elements import FeaturesSimple, X86Features
from libvirt_vmcfg.dom.elements import Memory
from libvirt_vmcfg.dom.elements import Metadata
from libvirt_vmcfg.dom.elements import Name
from libvirt_vmcfg.dom.elements import QemuOSConfig
from libvirt_vmcfg.dom.elements import PowerManagement
from libvirt_vmcfg.dom.elements import DomainUUID
from libvirt_vmcfg.dom.elements.devices import QemuAgentChannel
from libvirt_vmcfg.dom.elements.devices import Clock
from libvirt_vmcfg.dom.elements.devices import ConsolePTY
from libvirt_vmcfg.dom.elements.devices import CPU
from libvirt_vmcfg.dom.elements.devices import VirtIOMemballoon
from libvirt_vmcfg.dom.elements.devices import RNG
from libvirt_vmcfg.dom.elements.devices import QemuXHCIUSBController


def kvm_default_hardware(**kwargs) -> List[Element]:
    """
    Return a list containing the default elements of a typical libvirt VM.

    Two major things not included: interfaces or disks.
    """
    try:
        # Mandatory args
        memory: int = kwargs["memory"]
        name: str = kwargs["name"]
        vcpus: int = kwargs["vcpus"]
    except KeyError as e:
        raise ValueError(f"Value {e.args[0]} is required")

    # Optional args
    arch: str = kwargs.get("arch", "x86_64")
    boot_dev_order: Optional[Sequence[str]] = kwargs.get("boot_dev_order",
                                                         None)
    emulator_path: str = kwargs.get("emulator_path",
                                    "/usr/bin/qemu-system-x86_64")
    current_memory: int = kwargs.get("current_memory", memory)
    uuid: Union[str, UUID] = str(kwargs.get("uuid", uuid4()))
    metadata: Optional[etree._Element] = kwargs.get("metadata", None)

    features: Optional[FeaturesSimple]
    if arch in ("x86", "x86_64"):
        features = X86Features()
    else:
        features = None
        warn(f"Unknown architecture {arch}, features block may be "
             f"missing")

    # Begin construction
    devtree = [
        Emulator(emulator_path),
        Memory(memory, current_memory),
        Name(name),
        QemuOSConfig(arch, "q35", boot_dev_order),
        PowerManagement(),
        DomainUUID(uuid),
        QemuAgentChannel(),
        Clock(),
        ConsolePTY(),
        CPU(vcpus),
        VirtIOMemballoon(),
        RNG(),
        QemuXHCIUSBController(),
    ]

    if features is not None:
        devtree.append(features)

    if metadata is not None:
        devtree.append(Metadata(metadata))

    return devtree
