from enum import Enum
from urllib.parse import urlparse

from lxml import etree

from libvirt_vmcfg.domain.devices import Device


class DeviceType(Enum):
    DISK = "disk"
    CDROM = "cdrom"


class BusType(Enum):
    VIRTIO = "virtio"


class QemuDiskBlock(Device):
    unique = False

    def __init__(self, *, device, source_dev, target_dev,
                 target_bus=BusType.VIRTIO, readonly=False,
                 driver_attrs=None):
        self.device = device
        self.source_dev = source_dev
        self.target_dev = target_dev
        self.target_bus = target_bus
        self.readonly = readonly
        self.driver_attrs = driver_attrs if driver_attrs is not None else {}

    def attach_xml(self, root):
        # Check for existing target
        xpstr = f"/domain/devices/disk/target[@dev='{self.target_dev}']"
        if root.xpath(xpstr):
            raise ValueError("target device already attached")

        # Check for existing source, this would be a nasty conflict
        # (this should be safe if readonly tho)
        if not self.readonly:
            xpstr = f"/domain/devices/disk/source[@dev='{self.source_dev}']"
            if root.xpath(xpstr):
                raise ValueError("source device already attached")

        devices_tag = self.get_devices_tag(root)
        disk_tag = etree.SubElement(devices_tag, "disk", type="block",
                                    device=self.device.value)
        driver_tag = etree.SubElement(disk_tag, "driver", name="qemu")

        for key, value in self.driver_attrs.items():
            if value is None:
                continue
            elif value is True:
                value = "on"
            elif value is False:
                value = "off"
            elif not isinstance(value, str):
                value = str(value)

            driver_tag.attrib[key] = value

        etree.SubElement(disk_tag, "source", dev=self.source_dev)
        etree.SubElement(disk_tag, "target", dev=self.target_dev,
                         bus=self.target_bus.value)

        if self.readonly:
            etree.SubElement(disk_tag, "readonly")

        # lxml will clean up the rest :3
        return [disk_tag]

    def __repr__(self):
        return (f"QemuDiskBlock(device={self.device}, "
                f"source_dev={self.source_dev!r}, "
                f"target_dev={self.target_dev!r}, "
                f"target_bus={self.target_bus}, "
                f"readonly={self.readonly}, "
                f"driver_attrs={self.driver_attrs})")


class QemuDiskNet(Device):
    unique = False

    def __init__(self, *, device, source_url, target_dev,
                 target_bus=BusType.VIRTIO, readonly=True, driver_attrs=None):
        self.device = device
        self.source_url = source_url  # Used in __repr__
        self.target_dev = target_dev
        self.target_bus = target_bus
        self.readonly = readonly
        self.driver_attrs = driver_attrs if driver_attrs is not None else {}

        # Parse the URL
        up = urlparse(source_url, allow_fragments=False)
        if up.scheme not in ("http", "https"):
            raise ValueError("Unknown URL scheme", up.scheme)

        self.protocol =  up.scheme

        self.path = up.path
        if self.path and self.path != "/":
            self.path = self.path[1:]

        self.host, _, self.port = up.netloc.partition(":")
        if not self.port:
            self.port = None

    def attach_xml(self, root):
        # Check for existing target
        xpstr = f"/domain/devices/disk/target[@dev='{self.target_dev}']"
        if root.xpath(xpstr):
            raise ValueError("target device already attached")

        devices_tag = self.get_devices_tag(root)
        disk_tag = etree.SubElement(devices_tag, "disk", type="network",
                                    device=self.device.value)
        driver_tag = etree.SubElement(disk_tag, "driver", name="qemu")

        for key, value in self.driver_attrs.items():
            if value is None:
                continue
            elif value is True:
                value = "on"
            elif value is False:
                value = "off"
            elif not isinstance(value, str):
                value = str(value)

            driver_tag.attrib[key] = value

        source_tag = etree.SubElement(disk_tag, "source",
                                      protocol=self.protocol, name=self.path)
        host_tag = etree.SubElement(source_tag, "host", name=self.host)
        if self.port:
            host_tag.attrib["port"] = self.port

        etree.SubElement(disk_tag, "target", dev=self.target_dev,
                         bus=self.target_bus.value)

        if self.readonly:
            etree.SubElement(disk_tag, "readonly")

        # lxml will clean up the rest :3
        return [disk_tag]

    def __repr__(self):
        return (f"QemuDiskNet(device={self.device}, "
                f"source_url={self.source_url!r}, "
                f"target_dev={self.target_dev!r}, "
                f"target_bus={self.target_bus}, "
                f"readonly={self.readonly}, "
                f"driver_attrs={self.driver_attrs})")
