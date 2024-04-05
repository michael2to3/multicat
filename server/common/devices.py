from typing import Dict, List


class Devices:
    data: Dict

    def __init__(self, data: Dict):
        self.data = data

    def _extract_cuda_hip_devices(self, obj: Dict) -> List[Dict]:
        return obj.get("devices", [])

    def _extract_opencl_devices(self, obj: Dict) -> List[Dict]:
        devices = []
        for x in obj.get("platforms", []):
            devices += x.get("devices", [])
        return devices

    def get_generic_devices(self) -> List[Dict]:
        for x in ["cuda", "hip", "ocl"]:
            if obj := self.data.get(x):
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
                if bd[check] != ad[check]:
                    return False

        return True

