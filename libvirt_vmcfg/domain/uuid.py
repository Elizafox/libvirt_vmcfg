from uuid import UUID

from lxml import etree

from libvirt_vmcfg.domain import Element


class DomainUUID(Element):
    unique = True

    def __init__(self, uuid):
        if isinstance(uuid, UUID):
            self.uuid = str(uuid)
        else:
            # Validate
            self.uuid = str(UUID(uuid))

    def attach_xml(self, root):
        uuid_tag = etree.SubElement(root, "uuid")
        uuid_tag.text = str(self.uuid)
        return [uuid_tag]

    def __repr__(self):
        return f"DomainUUID({self.uuid!r})"
