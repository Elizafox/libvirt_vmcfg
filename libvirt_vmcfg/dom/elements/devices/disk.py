from abc import ABC, abstractmethod
from dataclasses import asdict, astuple, dataclass
from enum import Enum
from typing import Any, Dict, Optional, Sequence, cast
from urllib.parse import urlparse

from lxml import etree

from libvirt_vmcfg.dom.elements.devices import Device


class DeviceAttachment(Enum):
    DISK = "disk"
    CDROM = "cdrom"
    FLOPPY = "floppy"


class Tray(Enum):
    OPEN = "open"
    CLOSED = "closed"


class SourceVolumeMode(Enum):
    DIRECT = "direct"
    HOST = "host"


class TargetBus(Enum):
    VIRTIO = "virtio"
    SCSI = "scsi"
    IDE = "ide"
    SATA = "sata"
    USB = "usb"
    SD = "sd"


class Driver(Enum):
    # TODO: other driver types
    QEMU = "qemu"


class DriverType(Enum):
    RAW = "raw"
    BOCHS = "bochs"
    QCOW2 = "qcow2"
    QED = "qed"


class DriverCache(Enum):
    NONE = "none"
    DEFAULT = "default"
    WRITETHROUGH = "writethrough"
    WRITEBACK = "writeback"
    DIRECTSYNC = "directsync"
    UNSAFE = "unsafe"


class DriverIO(Enum):
    NATIVE = "native"
    THREADS = "threads"
    IO_URING = "io_uring"


class DriverErrorPolicy(Enum):
    STOP = "stop"
    REPORT = "report"
    IGNORE = "ignore"
    ENOSPACE = "enospace"


class DriverDiscard(Enum):
    UNMAP = "unmap"
    IGNORE = "ignore"


class DriverDetectZeroes(Enum):
    OFF = "off"
    ON = "on"
    UNMAP = "unmap"


@dataclass
class DriverOptions:
    """Basic driver data.

    There are a *lot* of flags for the driver tag, so they're encapsulated
    here.

    Variables left unset will be omitted from the final generated XML.
    """
    # TODO: more options
    driver: Driver
    type: Optional[DriverType] = None
    cache: Optional[DriverCache] = None
    io: Optional[DriverIO] = None
    error_policy: Optional[DriverErrorPolicy] = None
    rerror_policy: Optional[DriverErrorPolicy] = None
    ioeventfd: Optional[bool] = None
    event_idx: Optional[bool] = None
    copy_on_read: Optional[bool] = None
    discard: Optional[DriverDiscard] = None
    detect_zeroes: Optional[DriverDetectZeroes] = None
    queues: Optional[int] = None

    def __post_init__(self):
        if self.rerror_policy == DriverErrorPolicy.ENOSPACE:
            raise ValueError("rerror_policy cannot be ENOSPACE")


@dataclass
class IOTuneOptions:
    """Basic iotune options.

    This is only valid for Qemu."""
    total_bytes_sec: Optional[int] = None
    read_bytes_sec: Optional[int] = None
    write_bytes_sec: Optional[int] = None

    total_bytes_sec_max: Optional[int] = None
    read_bytes_sec_max: Optional[int] = None
    write_bytes_sec_max: Optional[int] = None

    total_iops_sec: Optional[int] = None
    read_iops_sec: Optional[int] = None
    write_iops_sec: Optional[int] = None

    total_iops_sec_max: Optional[int] = None
    read_iops_sec_max: Optional[int] = None
    write_iops_sec_max: Optional[int] = None

    total_bytes_sec_max_length: Optional[int] = None
    read_bytes_sec_max_length: Optional[int] = None
    write_bytes_sec_max_length: Optional[int] = None

    total_iops_sec_max_length: Optional[int] = None
    read_iops_sec_max_length: Optional[int] = None
    write_iops_sec_max_length: Optional[int] = None

    size_iops_sec: Optional[int] = None

    group_name: Optional[str] = None

    def __post_init__(self):
        # There's no reason to have these functions be global.
        def test_attr_only_one(*attrs: str) -> None:
            assert len(attrs) > 1
            attrs_value = tuple(getattr(self, a) for a in attrs)
            if attrs_value.count(None) < (len(attrs_value) - 1):
                raise ValueError("Attributes are mutually exclusive", attrs,
                                 *attrs_value)

        def test_attr_require(dependent: str, requires: str) -> None:
            dependent_value = getattr(self, dependent)
            requires_value = getattr(self, requires)

            if dependent_value is not None and requires_value is None:
                raise ValueError(f"Dependent value requires value to be set",
                                 dependent, requires, dependent_value,
                                 requires_value)

        test_attr_only_one("total_bytes_sec", "read_bytes_sec",
                            "write_bytes_sec")
        test_attr_only_one("total_iops_sec", "read_iops_sec",
                            "write_iops_sec")
        test_attr_only_one("total_bytes_sec_max", "read_bytes_sec_max",
                            "write_bytes_sec_max")
        test_attr_only_one("total_iops_sec_max", "read_iops_sec_max",
                            "write_iops_sec_max")
        test_attr_require("total_bytes_sec_max_length", "total_bytes_sec_max")
        test_attr_require("read_bytes_sec_max_length", "read_bytes_sec_max")
        test_attr_require("write_bytes_sec_max_length", "write_bytes_sec_max")
        test_attr_require("total_iops_sec_max_length", "total_iops_sec_max")
        test_attr_require("read_iops_sec_max_length", "read_iops_sec_max")
        test_attr_require("write_iops_sec_max_length", "write_iops_sec_max")


class DiskSource(ABC):
    """Interface for disk sources.

    Sources can be incredibly complex, so we use a special object that can help
    us construct it.
    """
    @abstractmethod
    def attach_xml(self, disk_tag: etree._Element) -> None:
        # Implement this method in your subclass.
        #
        # WARNING WARNING WARNING:
        # Do your validation in __init__! Failure to do so will result in a
        # gigantic mess of a half-setup disk tag. This is bad!
        raise NotImplementedError


class DiskSourceBlockPath(DiskSource):
    """Block source for disk."""
    def __init__(self, path: str):
        self.path = path

    def attach_xml(self, disk_tag: etree._Element) -> None:
        disk_tag.set("type", "block")
        etree.SubElement(disk_tag, "source", dev=self.path)

    def __repr__(self):
        return f"DiskSourceBlockPath(path={self.path!r})"


class DiskSourceNetHTTP(DiskSource):
    """HTTP(S) source for disk."""
    def __init__(self, url: str, *,
                 cookies: Optional[Dict[str, str]] = None, readahead: int = 0,
                 timeout: int = 0, ssl_verify: Optional[bool] = None):
        self.url = url
        self.cookies = cookies
        self.readahead = readahead
        self.timeout = timeout
        self.ssl_verify = ssl_verify

        # Parse the URL
        up = urlparse(url, allow_fragments=False)
        if up.scheme not in ("http", "https"):
            raise ValueError("Invalid URL scheme", up.scheme)

        self.protocol = up.scheme

        self.path = up.path
        if self.path and self.path != "/":
            self.path = self.path[1:]

        self.port: Optional[str]
        self.host, _, self.port = up.netloc.partition(":")
        if not self.port:
            self.port = None

        self.query = up.query if up.query else None

    def attach_xml(self, disk_tag: etree._Element):
        disk_tag.set("type", "network")

        source_tag = etree.SubElement(disk_tag, "source",
                                      protocol=self.protocol, name=self.path)

        host_tag = etree.SubElement(source_tag, "host", name=self.host)
        if self.port:
            host_tag.set("port", str(self.port))

        if self.query:
            host_tag.set("query", self.query)

        if self.cookies:
            cookies_tag = etree.SubElement(source_tag, "cookies")
            for k, v in cookies_tag.items():
                cookie_tag = etree.SubElement(cookies_tag, "cookie", name=k)
                cookie_tag.text = v

        if self.readahead > 0:
            etree.SubElement(source_tag, "readahead", size=str(self.readahead))

        if self.timeout > 0:
            etree.SubElement(source_tag, "timeout", seconds=str(self.timeout))

        if self.ssl_verify is not None and self.protocol == "https":
            etree.SubElement(source_tag, "ssl",
                             verify=("yes" if self.ssl_verify else "no"))

    def __repr__(self):
        return (f"DiskSourceNetHTTP(url={self.url!r}, "
                f"cookies={self.cookies!r}, readahead={self.readahead!r}, "
                f"timeout={self.timeout!r}, ssl_verify={self.ssl_verify!r}")


class DiskSourceVolume(DiskSource):
    """libvirt volume storage for disks."""
    def __init__(self, pool: str, volume: str,
                 mode: Optional[SourceVolumeMode] = None):
        self.pool = pool
        self.volume = volume
        self.mode = mode

    def attach_xml(self, disk_tag: etree._Element):
        disk_tag.set("type", "volume")

        source_tag = etree.SubElement(disk_tag, "source", pool=self.pool,
                                      volume=self.volume)
        # For when we get iSCSI support
        #if self.mode is not None:
        #    source_tag.set("mode", self.mode.value)


class DiskTarget:
    """
    Class for disk targets.

    These are much simpler than disk sources, so this does not require an
    interface.
    """
    def __init__(self, device: DeviceAttachment, path: str, *,
                 bus: Optional[TargetBus] = None, tray: Optional[Tray] = None,
                 removable: Optional[bool] = None):
        if (device not in (DeviceAttachment.CDROM, DeviceAttachment.FLOPPY)
                and tray is not None):
            raise ValueError("tray is only valid with CDROM and Floppy",
                             device, tray)
        elif bus != TargetBus.USB and removable is not None:
            raise ValueError("Only USB devices may be removable", device,
                             removable)

        # TODO: validate the dev parameter

        self.device = device
        self.path = path
        self.bus = bus
        self.tray = tray
        self.removable = removable

    def __repr__(self):
        return (f"DiskTarget(device={self.device!r}, path={self.path!r}, "
                f"bus={self.bus!r}, tray={self.tray!r}, "
                f"removable={self.removable!r})")


def DiskTargetCDROM(path: str, **kwargs) -> DiskTarget:
    """Factory for generating cdrom targets."""
    return DiskTarget(DeviceAttachment.CDROM, path, **kwargs)


def DiskTargetDisk(path: str, **kwargs) -> DiskTarget:
    """Factory for generating disk targets."""
    return DiskTarget(DeviceAttachment.DISK, path, **kwargs)


def DiskTargetFloppy(path: str, **kwargs) -> DiskTarget:
    """Factory for generating floppy targets."""
    return DiskTarget(DeviceAttachment.FLOPPY, path, **kwargs)


class Disk(Device):
    unique: bool = False

    def __init__(self, source: DiskSource, target: DiskTarget,
                 driver_opts: DriverOptions, readonly: bool = False,
                 iotune_opts: Optional[IOTuneOptions] = None):
        self.source = source
        self.target = target
        self.driver_opts = driver_opts
        self.readonly = readonly
        self.iotune_opts = iotune_opts

    def _populate_driver_tag(self, driver_tag: etree._Element) -> None:
        # This is a quick and dirty hack for iterating over the driver_opts
        # items. This helps facilitate my laziness. ;p --Elizafox
        driver_dict = asdict(self.driver_opts)
        for attr, value in driver_dict.items():
            if attr == "driver" or value is None:
                # XXX hack!
                continue

            # Coerce into correct type
            if isinstance(value, int):
                value = str(value)
            elif isinstance(value, bool):
                value = ("on" if value else "off")
            elif isinstance(value, Enum):
                value = value.value
            elif isinstance(value, str):
                pass
            else:
                # Really shouldn't happen.
                raise ValueError("Unexpected value type", type(value))

            # At this point, we should certainly have a value
            driver_tag.set(attr, value)

    def attach_xml(self, root: etree._Element) -> Sequence[etree._Element]:
        # Check for existing target, to avoid conflicts.
        # Do this before actual tag creation, to avoid making a mess.
        xpstr = f"/domain/devices/disk/target[@dev='{self.target.path}']"
        if root.xpath(xpstr):
            raise ValueError("target device already attached")

        devices_tag = self.get_devices_tag(root)
        disk_tag = etree.SubElement(devices_tag, "disk", type="block",
                                    device=self.target.device.value)

        # Set up the driver
        driver_tag = etree.SubElement(disk_tag, "driver",
                                      name=self.driver_opts.driver.value)
        try:
            self._populate_driver_tag(driver_tag)
        except Exception as e:
            # Well, crap. This really shouldn't have happened.
            # Clean up our mess and get out of here.
            #
            # XXX - hack alert! Icky! This is an implementation detail!
            self.detach_xml([disk_tag])
            raise AssertionError("Invalid driver options",
                                 self.driver_opts) from e

        # Now we have the source set itself up.
        # NOTE: sources are a LOT more involved than just "add a source tag
        # and be done with it", because that's how libvirt works. This is why
        # sources do their own setup.
        self.source.attach_xml(disk_tag)

        # Targets are simple, so we can do that setup ourselves.
        # We assume the target device did parameter validation, so no need for
        # error checking here.
        target_tag = etree.SubElement(disk_tag, "target", dev=self.target.path)

        if self.target.bus is not None:
            target_tag.set("bus", self.target.bus.value)

        if self.target.tray is not None:
            target_tag.set("tray", self.target.tray.value)

        if self.target.removable is not None:
            target_tag.set("removable",
                           ("yes" if self.target.removable else "no"))

        # Any iotune options?
        if (self.iotune_opts is not None
                and astuple(self.iotune_opts).count(None) > 0):
            iotune_tag = etree.SubElement(disk_tag, "iotune")
            for attr, value in asdict(self.iotune_opts).items():
                if value is None:
                    continue

                tag = etree.SubElement(iotune_tag, attr)
                tag.text = str(value)

        if self.readonly:
            etree.SubElement(disk_tag, "readonly")

        # lxml will clean up the rest :3
        return [disk_tag]

    def __repr__(self):
        return (f"Disk(source={self.source!r}, "
                f"target={self.target!r}, "
                f"driver_opts={self.driver_opts!r}, "
                f"readonly={self.readonly})")
