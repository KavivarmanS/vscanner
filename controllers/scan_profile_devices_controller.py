from models.scan_profile_devices_model import ScanProfileDevice

class ScanProfileDeviceController:
    def __init__(self):
        self.model = ScanProfileDevice()

    def add_scan_profile_device(self, profile_id, device_id):
        return self.model.add(profile_id, device_id)

    def get_all_scan_profile_devices(self):
        return self.model.get_all()

    def delete_scan_profile_device(self, profile_id, device_id):
        self.model.delete(profile_id, device_id)
