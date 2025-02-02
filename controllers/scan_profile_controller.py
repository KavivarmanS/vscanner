from models.scan_profile_model import ScanProfile


class ProfileController:
    def __init__(self):
        self.model = ScanProfile()

    def add_profile(self, user_id, scan_frequency):
        self.model.create_profile(user_id, scan_frequency)

    def get_profiles(self):
        return self.model.read_profiles()

    def get_profiles_by_id(self, profile_id):
        return self.model.read_profiles_by_id(profile_id)

    def get_profiles_by_user_id(self, user_id):
        return self.model.read_profiles_by_user_id(user_id)

    def modify_profile(self, profile_id, user_id, scan_frequency):
        self.model.update_profile(profile_id, user_id, scan_frequency)

    def remove_profile(self, profile_id):
        self.model.delete_profile(profile_id)
