from models.scan_profile_model import ScanProfile
from models.scan_profile_devices_model import ScanProfileDevice
from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities


class ProfileController:
    def __init__(self):
        self.model = ScanProfile()
        self.device_model = ScanProfileDevice()
        self.vulnerabilities_model = ScanProfileVulnerabilities()

    def add_profile(self, user_id):
        self.model.create_profile(user_id)

    def get_profiles(self):
        return self.model.read_profiles()

    def get_profiles_by_id(self, profile_id):
        return self.model.read_profiles_by_id(profile_id)

    def get_profiles_by_user_id(self, user_id):
        return self.model.read_profiles_by_user_id(user_id)

    def modify_profile(self, profile_id, user_id):
        self.model.update_profile(profile_id, user_id)

    def remove_profile(self, profile_id):
        self.model.delete_profile(profile_id)

    def get_devices_by_profile(self,profile_id):
        return self.device_model.get_device_by_profile_id(profile_id)

    def get_vulnerabilities_by_profile(self,profile_id):
        return self.vulnerabilities_model.get_vulnerabilities_by_profile_id(profile_id)

    def add_devices(self,profile_id, device_id):
        self.device_model.add(profile_id, device_id)

    def remove_devices(self,profile_id, device_id):
        self.device_model.delete(profile_id, device_id)

    def add_vulnerabilities(self, profile_id, vulnerability_id):
        self.vulnerabilities_model.add(profile_id,vulnerability_id)

    def remove_vulnerabilities(self, profile_id, vulnerability_id):
        self.vulnerabilities_model.delete(profile_id, vulnerability_id)
