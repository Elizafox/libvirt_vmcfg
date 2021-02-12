from string import ascii_lowercase
from typing import Dict, Iterable

"""Disk utilities for libvirt_vmcfg."""

qemu_driver_attrs_raw: Dict[str, str] = {
    "type": "raw",
    "cache": "none",
    "io": "native",
}
"""Recommended values to pass to QemuDiskBlock or QemuDiskNet."""


def base26(value: int) -> str:
    """Convert a given value to base26."""
    if value < 0:
        raise ValueError("Cannot convert negative value to base26", value)

    string = []
    while value >= 0:
        value, rem = divmod(value, 26)
        value -= 1
        string.append(ascii_lowercase[rem])

    return "".join(reversed(string))


def disk_letter(prefix: str, start: int = 0) -> Iterable[str]:
    """A generator that generates disk names derived from letters.

    An example of this is "vda"
    """
    while True:
        yield f"{prefix}{base26(start)}"
        start += 1


def disk_number(prefix: str, start: int = 0) -> Iterable[str]:
    """A generator that generates disk names derived from numbers.

    An example of this is "sr0"
    """
    while True:
        yield f"{prefix}{start}"
        start += 1
