*************************************************************
``libvirt_vmcfg.dom.profiles``: Canned domain profile helpers
*************************************************************

########
Synopsis
########
The goal of this particular module is to help you build lists of elements you
can then add to domains. It's designed to only output elements that almost
everyone can agree on.

###
API
###

============
linux_virtio
============
.. py:module:: libvirt_vmcfg.dom.profiles.linux_virtio

.. py:function:: kvm_default_hardware(**kwargs) -> List[Element]:

   :synopsis: Generate default hardware for Linux VirtIO domains.
   :key int memory: Amount of memory for the domain (required)
   :key str name: Name for the domain (required)
   :key int vcpus: Number of VCPUs to allocate to domain (required)
   :key str arch: Architecture (default ``"x86_64"``)
   :key Sequence[str] boot_dev_order: Sequence of strings specifying
                                      the boot order (default: undefined)
   :key str emulator_path: Path to the emulator (default:
                           ``/usr/bin/qemu-system-{arch}``)
   :key int current_memory: Amount of memory to allocate to the domain
                            initally (default: same as memory)
   :key Union[str, python.uuid.UUID] uuid: UUID for the domain (default:
                                           randomly generated via
                                           :py:func:`~python:uuid.uuid4`)
   :key lxml.etree._Element metadata: metadata tag to pass in (default:
                                      undefined)

   Generate a default list of
   :py:class:`~libvirt_vmcfg.dom.elements.Element` s for Linux VirtIO guests.
   This list may be suited for other operating systems, but they have not been
   tested.

   .. tip:: No disks or interfaces are attached. You can attach those by
            appending your own elements to the end of the returned list.
