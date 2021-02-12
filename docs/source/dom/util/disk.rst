****************************************************
``libvirt_vmcfg.dom.util``: Domain utility functions
****************************************************

########
Synopsis
########
This module contains miscellaneous utility classes, functions, and other bits
for constructing domains.

###
API
###
.. py:module:: libvirt_vmcfg.dom.util.disk

.. py:function:: disk_letter(prefix: str, start: int = 0) -> Iterator[str]

   :param str prefix: String to prefix the drive names with, such as ``"vd"``.
   :param int start: Drive number to start from. 0 is a, 1 is b, etc.
   :return: A generator function that yields strings and returns nothing.

   A generator that creates an infinite stream of values for drive names.
   This is useful for domain drive targets.

   Example:

   .. code-block:: python

      disk_gen = disk_letter("vd")
      print(next(disk_gen))  # "vda"
      print(next(disk_gen))  # "vdb"

   This function also handles drives over 26 gracefully:

   .. code-block:: python

      disk_gen = disk_letter("sd", 25)
      print(next(disk_gen))  # sdz
      print(next(disk_gen))  # sdaa


.. py:function:: disk_number(prefix: str, start: int = 0) -> Iterator[str]

   :param str prefix: String to prefix the drive names with, such as ``"sr"``.
   :param int start: Drive number to start with.
   :return: A generator function that yields strings and returns nothing.

   A generator that creates an infinite stream of values for drive names.
   This is useful for domain drive targets.

   Example:

   .. code-block:: python

      disk_gen = disk_number("sr")
      print(next(disk_gen))  # "sr0"
      print(next(disk_gen))  # "sr1"
      ...
