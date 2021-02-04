libvirt\_vmcfg
--------------
`libvirt_vmcfg` is a library for generating XML VM specifications for use in libvirt.

It's in an alpha state but pull requests welcome.

Documentation is poor at the moment as I have other priorities. When I have time, I will create better docs, I promise.

Example
=======
```python
from lxml import etree
  
from libvirt_vmcfg.profiles.linux_virtio import kvm_default_hardware
from libvirt_vmcfg.devices.interface import BridgedInterface
from libvirt_vmcfg.devices.disk import QemuDiskBlock, QemuDiskNet, DeviceType
from libvirt_vmcfg.util.disk import TargetDevGenerator, qemu_driver_attrs_raw
from libvirt_vmcfg import Domain


# Automatic generator for target devices
t = TargetDevGenerator()

# Shorthand for creating the devices we need, based on what virt-install does
# This doesn't do everything - you still need disks and a network interface.
# You can also create your own hardware specification, see
# libvirt_vmcfg/profiles/linux_virtio.py for details.
elements = kvm_default_hardware(name="test", vcpus=2, memory=786432,
                                boot_dev_order=["hd"])

# This is the hard disk specification, using a block device
# Note how we use qemu_driver_attrs_raw here, these are the recommended
# parameters for a raw device with QEMU
hard_disk = QemuDiskBlock(device=DeviceType.DISK,
                          source_dev="/dev/foo-vg/lvm_disk_partition",
                          target_dev=t.next_virtio(),
                          driver_attrs=qemu_driver_attrs_raw)

# This is the CD specification
cdrom = QemuDiskNet(device=DeviceType.CDROM,
                    source_url="http://example.com/install/cloudinit-seed.iso",
                    target_dev=t.next_virtio(), readonly=True)

# Network interface, only bridging is supported right now
interface = BridgedInterface("br0")

# Obvious
elements.extend((hard_disk, cdrom, interface))

# Create our domain and emit the XML
# Since this is an example, we print it out
dom = Domain(elements=elements)
print(dom.emit_xml(pretty_print=True))
```

TODO
====
A lot. I'll get around to most of these eventually. I hope. I'm sadly quite busy these days.
* More interface types
* More disk types, like LUNs
* More hardware profiles, like for Windows, old Linux, BSD, etc.
* More hardware that isn't virtio
* More hardware, period
* More hardware options, like more timers, etc.
* More hypervisors (Xen, VirtualBox, VMWare Workstation, and ESXi are probably the only other relevant ones)
* Investigate other architectures, like ppc64le and aarch64, add relevant bits from those
* Creation of XML for volumes
* Documentation
* Find a better way to handle `driver_attrs` with disks
* Find a clean way to add all the relevant doodads from the (very complicated) disk specification
* A meaningful `repr` implementation for elements and the domain

License
=======
CC0 public domain dedication. Do whatever you want with it.

Say thanks
==========
You can thank me at [my Say Thanks](https://saythanks.io/to/elizabeth.jennifer.myers%40gmail.com).

You can also [donate](https://paypal.me/Elizafox) to help keep me afloat during these tough times.
