from typing import Union

from lxml import etree


class Volume:
    """
    Basic libvirt volume information.

    Attributes:
      name: name of the volume
      capacity: capacity of the volume in bytes
    """

    def __init__(self, name: str, capacity: int):
        """
        Create a volume object.

        Parameters:
          name: name of the volume
          capacity: capacity of the volume in bytes
        """
        self.name = name
        self.capacity = capacity

    def emit_xml(self, *, pretty_print: bool = False,
                 encoding: str = "unicode") -> Union[str, bytes]:
        """
        Emit libvirt XML document for the volume.

        Parameters:
          pretty_print: whether or not to pretty print the result
          encoding: encoding of the resulting data, set to "unicode" for UTF-8
        """
        volume_tag = etree.Element("volume")

        name_tag = etree.SubElement(volume_tag, "name")
        name_tag.text = self.name

        capacity_tag = etree.SubElement(volume_tag, "capacity")
        capacity_tag.text = str(self.capacity)

        return etree.tostring(volume_tag, pretty_print=pretty_print,
                              encoding=encoding)

