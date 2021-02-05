from uuid import uuid4

from libvirt_vmcfg import Domain

from libvirt_vmcfg.emulator import Emulator
from libvirt_vmcfg.features import X86Features
from libvirt_vmcfg.memory import Memory
from libvirt_vmcfg.metadata import Metadata
from libvirt_vmcfg.name import Name
from libvirt_vmcfg.osconfig import QemuOSConfig
from libvirt_vmcfg.power_management import PowerManagement
from libvirt_vmcfg.uuid import DomainUUID
from libvirt_vmcfg.devices.channel import QemuAgentChannel
from libvirt_vmcfg.devices.clock import Clock
from libvirt_vmcfg.devices.console import ConsolePTY
from libvirt_vmcfg.devices.cpu import CPU
from libvirt_vmcfg.devices.memballoon import VirtIOMemballoon
from libvirt_vmcfg.devices.rng import RNG
from libvirt_vmcfg.devices.usb import QemuXHCIUSBController


def kvm_default_hardware(**kwargs):
    """
    Return a list containing the default elements of a typical libvirt VM.

    Two major things not included: interfaces or disks.
    """
    try:
        # Mandatory args
        memory = kwargs["memory"]
        name = kwargs["name"]
        vcpus = kwargs["vcpus"]
    except KeyError as e:
        raise ValueError(f"Value {e.args[0]} is required")

    # Optional args
    arch = kwargs.get("arch", "x86_64")
    boot_dev_order = kwargs.get("boot_dev_order", None)
    emulator_path = kwargs.get("emulator_path", "/usr/bin/qemu-system-x86_64")
    current_memory = kwargs.get("current_memory", memory)
    uuid = kwargs.get("uuid", str(uuid4()))
    metadata = kwargs.get("metadata", None)

    if arch in ("x86", "x86_64"):
        features = X86Features()
    else:
        warnings.warn(f"Unknown architecture {arch}, features block may be "
                      f"missing")

    # Begin construction
    devtree = [
        Emulator(emulator_path),
        features,
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
    return devtree
