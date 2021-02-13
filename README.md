libvirt\_vmcfg
--------------
`libvirt_vmcfg` is a library for generating XML VM specifications for use in libvirt.

It's in an alpha state but pull requests welcome.

Documentation is poor at the moment as I have other priorities. When I have time, I'll create better docs.

Examples
=======

### Domain builder
```python
from lxml import etree

from libvirt_vmcfg.dom.profiles.linux_virtio import kvm_default_hardware
from libvirt_vmcfg.dom.elements.devices import BridgedInterface
from libvirt_vmcfg.dom.elements.devices import DiskTargetCDROM, DiskTargetDisk
from libvirt_vmcfg.dom.elements.devices import (DiskSourceBlockPath,
                                                DiskSourceNetHTTP, TargetBus)
from libvirt_vmcfg.dom.elements.devices import (Driver, DriverType,
                                                DriverCache, DriverIO,
                                                DriverOptions)
from libvirt_vmcfg.dom.elements.devices import Disk
from libvirt_vmcfg.dom.util.disk import disk_letter
from libvirt_vmcfg.dom import Domain


dev = disk_letter("vd")

elements = kvm_default_hardware(name="poopty", vcpus=2, memory=64*(1024**2),
                                boot_dev_order=["hd"])

# Build up the disk
source_disk = DiskSourceBlockPath("/dev/zeta-vg/debian-test-01")
target_disk = DiskTargetDisk(next(dev), bus=TargetBus.VIRTIO)
driver_opts_disk = DriverOptions(driver=Driver.QEMU, type=DriverType.RAW,
                                 cache=DriverCache.NONE, io=DriverIO.NATIVE)
disk = Disk(source_disk, target_disk, driver_opts_disk, False)

# Now the CD
source_http = DiskSourceNetHTTP("http://localhost/install/install.iso")
target_cdrom = DiskTargetCDROM(next(dev), bus=TargetBus.VIRTIO)
driver_opts_cdrom = DriverOptions(driver=Driver.QEMU)
cdrom = Disk(source_http, target_cdrom, driver_opts_cdrom, True)

# Specify the Interface
interface = BridgedInterface("br0")

elements.extend((disk, cdrom, interface))

d = Domain(elements=elements)
print(repr(d))
print(d.emit_xml(pretty_print=True))
```

### Volumes
```python
from libvirt_vmcfg.vol import Volume


GIGABYTE = 1073741824

# Note the default unit for volumes is gigabytes
vol = Volume(name="test", size=3 * GIGABYTE)
print(vol.emit_xml(pretty_print=True))
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
  * Ensure hypervisor portability
* Investigate other architectures, like ppc64le and aarch64, add relevant bits from those
  * Ensure portability to said platforms
* Documentation
* Make `volume` interoperate with `domain` where relevant
* Flesh out `vol` module

Contributions
=============
See the [contributing file](CONTRIBUTING.md) for more information.

License
=======
[CC0](LICENSE), dedicated to the public domain. Do whatever you want with it.

Unfortunately I have to say this, because this comes up a lot in other projects. Let me make it clear: the project "licensing" (insofar a public domain dedication can be considered a license) is not up for debate. I wanted CC0 and it was a deliberate thoughtful choice. I am fully aware of its ramifications and have no intention to reverse my course on the matter. I was not — nor am not — willing or even able to enforce any restrictions on people or companies. Just do what you want with this. Relicensing is allowed; you may do so if you wish. Or don't. I don't care one way or the other.

Say thanks
==========
You can thank me at [my Say Thanks](https://saythanks.io/to/elizabeth.jennifer.myers%40gmail.com).

You can also [donate](https://paypal.me/Elizafox) to help keep me afloat during these tough times.
