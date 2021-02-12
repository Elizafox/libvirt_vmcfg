.. libvirt_vmcfg documentation master file, created by
   sphinx-quickstart on Sun Feb  7 23:23:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _`libvirt`: https://libvirt.org/

*****************************************
Welcome to libvirt_vmcfg's documentation!
*****************************************
``libvirt_vmcfg`` is a package designed to help generate `libvirt`_ XML
configuration easily.

This project is still in an alpha state, so expect improvements as time goes
on!

Quick example:

.. code-block:: python

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


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   dom/domain.rst
   dom/elements.rst
   dom/profiles.rst
   dom/util/disk.rst
   vol/volume.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
