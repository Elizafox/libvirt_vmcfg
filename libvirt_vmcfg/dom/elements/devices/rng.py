from enum import Enum
from typing import Sequence

from lxml import etree

from libvirt_vmcfg.dom.elements.devices import Device


class RNGModel(Enum):
    VIRTIO = "virtio"


class RNG(Device):
    unique: bool = False

    def __init__(self, model: RNGModel = RNGModel.VIRTIO,
                 backend_dev: str = "/dev/urandom"):
        self.model = model
        self.backend_dev = backend_dev

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        devices_tag = self.get_devices_tag(root)
        rng_tag = etree.SubElement(devices_tag, "rng", model=self.model.value)
        backend_tag = etree.SubElement(rng_tag, "backend", model="random")
        backend_tag.text = self.backend_dev
        return [rng_tag, backend_tag]

    def __repr__(self):
        return f"RNG(model={self.model}, backend_dev={self.backend_dev!r})"
