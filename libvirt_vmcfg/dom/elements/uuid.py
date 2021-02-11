from typing import Sequence, Union
from uuid import UUID

from lxml import etree

from libvirt_vmcfg.dom.elements import Element


class DomainUUID(Element):
    unique: bool = True

    def __init__(self, uuid: Union[UUID, str]):
        self.uuid: str
        if isinstance(uuid, UUID):
            self.uuid = str(uuid)
        else:
            # Validate
            self.uuid = str(UUID(uuid))

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        uuid_tag = etree.SubElement(root, "uuid")
        uuid_tag.text = str(self.uuid)
        return [uuid_tag]

    def __repr__(self):
        return f"DomainUUID({self.uuid!r})"
