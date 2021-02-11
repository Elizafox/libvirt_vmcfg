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
   from libvirt_vmcfg.dom.elements.devices import QemuDiskBlock, QemuDiskNet, DeviceType
   from libvirt_vmcfg.dom.util.disk import TargetDevGenerator, qemu_driver_attrs_raw
   from libvirt_vmcfg.dom import Domain


   t = TargetDevGenerator()

   elements = kvm_default_hardware(name="poopty", vcpus=2, memory=64*(1024**2),
                                   boot_dev_order=["hd"])

   hard_disk = QemuDiskBlock(device=DeviceType.DISK,
                             source_dev="/dev/zeta-vg/debian-test-01",
                             target_dev=t.next_virtio(),
                             driver_attrs=qemu_driver_attrs_raw)

   cdrom = QemuDiskNet(device=DeviceType.CDROM,
                       source_url="http://localhost/install/install.iso",
                       target_dev=t.next_virtio(), readonly=True)

   interface = BridgedInterface("br0")

   elements.extend((hard_disk, cdrom, interface))

   d = Domain(elements=elements)
   print(repr(d))
   print(d.emit_xml(pretty_print=True))

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   dom/domain.rst
   dom/elements.rst
   dom/profiles.rst
   vol/volume.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
