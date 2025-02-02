from models.vulnerabilities_in_scan_result_model import VulnerabilitiesInScanResultModel

class VulnerabilitiesInScanResultController:
    def __init__(self):
        self.model = VulnerabilitiesInScanResultModel()

    def add_vulnerability(self, result_id, vulnerability_id):
        return self.model.add(result_id, vulnerability_id)

    def get_all_vulnerabilities(self):
        return self.model.get_all()

    def delete_vulnerability(self, result_id, vulnerability_id):
        return self.model.delete(result_id, vulnerability_id)
