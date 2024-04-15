from typing import Dict, List, TypedDict


class DeviceInfo(TypedDict):
    device_id: str
    device_name: str
    device_processors: int


class DeviceCategory(TypedDict, total=False):
    devices: List[DeviceInfo]
    platforms: List[Dict]


class Devices:
    data: Dict[str, DeviceCategory]

    def __init__(self, data: Dict[str, DeviceCategory]):
        self.data = data

    def get_generic_devices(self) -> List[DeviceInfo]:
        for category in ["cuda", "hip", "ocl"]:
            if obj := self.data.get(category):
                if "devices" in obj:
                    return self._extract_cuda_hip_devices(obj)
                else:
                    return self._extract_opencl_devices(obj)
        return []

    def __eq__(self, other) -> bool:
        devices_before = self.get_generic_devices()
        devices_after = other.get_generic_devices()

        if len(devices_before) != len(devices_after):
            return False

        checks = ["device_id", "device_name", "device_processors"]

        for bd, ad in zip(devices_before, devices_after):
            for check in checks:
                if bd.get(check) != ad.get(check):
                    return False

        return True

    def _extract_cuda_hip_devices(self, obj: DeviceCategory) -> List[DeviceInfo]:
        return obj.get("devices", [])

    def _extract_opencl_devices(self, obj: DeviceCategory) -> List[DeviceInfo]:
        devices: List[DeviceInfo] = []
        for platform in obj.get("platforms", []):
            devices.extend(platform.get("devices", []))
        return devices
