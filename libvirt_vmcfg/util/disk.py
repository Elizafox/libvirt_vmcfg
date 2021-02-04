"""Disk utilities for libvirt_vmcfg."""

"""Recommended values to pass to QemuDiskBlock or QemuDiskNet."""
qemu_driver_attrs_raw = {
    "type": "raw",
    "cache": "none",
    "io": "native",
}

class TargetDevGenerator:
    """Generator for device names, for use in target_dev blocks."""
    def __init__(self, *, start_ide=1, start_virtio=1, start_scsi=1,
                 start_sr=0, start_nvme=0):
        self.start_ide = start_ide
        self.start_virtio = start_virtio
        self.start_scsi = start_scsi
        self.start_sr = start_sr
        self.start_nvme = start_nvme

    @staticmethod
    def _dev_letter(value):
        if value <= 0:
            raise ValueError("Invalid value encountered for drive letter")

        string = []
        while value > 0:
            value, rem = divmod(value, 26)
            if rem == 0:
                value -= 1
                rem += 26
            char = chr(rem + ord('a') - 1)
            string.append(char)

        return "".join(reversed(string))

    def next_ide(self):
        value = self._dev_letter(self.start_ide)
        self.start_ide += 1
        return f"hd{value}"

    def next_virtio(self):
        value = self._dev_letter(self.start_virtio)
        self.start_virtio += 1
        return f"vd{value}"

    def next_scsi(self):
        value = self._dev_letter(self.start_scsi)
        self.start_scsi += 1
        return f"sd{value}"

    def next_sr(self):
        value = self.start_sr
        self.start_sr += 1
        return f"sr{value}"

    def next_nvme(self):
        value = self.start_nvme
        self.start_nvme += 1
        return f"nvme{value}"
