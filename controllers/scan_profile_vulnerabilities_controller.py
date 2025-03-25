from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities

class ScanProfileVulnerabilitiesController:
    def __init__(self):
        self.model = ScanProfileVulnerabilities()

    def add_scan_profile_vulnerability(self, profile_id, vulnerability_id):
        return self.model.add(profile_id, vulnerability_id)

    def get_all_scan_profile_vulnerabilities(self):
        return self.model.get_all()

    def get_vulnerabilities_by_profile_id(self, profile_id):
        return self.model.get_vulnerabilities_by_profile_id(profile_id)

    def delete_scan_profile_vulnerability(self, profile_id, vulnerability_id):
        return self.model.delete(profile_id, vulnerability_id)


