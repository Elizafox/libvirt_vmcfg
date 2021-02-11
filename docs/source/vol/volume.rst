*******************************************
``libvirt_vmcfg.vol``: Basic volume support
*******************************************

########
Synopsis
########
This module contains rudimentary XML generation for volumes. It's very much in
a basic state, but may be of some use to some.

###
API
###
.. py:module:: libvirt_vmcfg.vol

======
Volume
======

.. py:class:: Volume(name: str, capacity: int)

   :synopsis: Basic volume information.
   :param str name: Name of the volume.
   :param int capacity: Capacity of the volume in bytes.

   .. py:method:: emit_xml(*, pretty_print: bool = False, encoding: \
                           str = "unicode") -> Union[str, bytes]

      :synopsis: Emit libvirt XML document for the volume.
      :param bool pretty_print: Whether or not the resulting text should be
                                formatted for pretty printing.
      :param str encoding: The encoding of the resulting XML string emitted,
                           if set to ``None``, ``bytes`` will be emitted.

      Emit XML based on volume information.

      This method is :wikipedia-en:`idempotent <Idempotence>`.
