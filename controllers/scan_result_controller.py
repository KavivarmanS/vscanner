from models.scan_result_model import ScanResultModel
from datetime import date
from controllers.scan_controller import ScanController

class ScanResultController:
    def __init__(self):
        self.model = ScanResultModel()


    def add_scan_result(self, profile_id):
        scan_date = date.today()
        scan_controller = ScanController()
        result = scan_controller.scan_for_cves(profile_id)
        return self.model.add(profile_id, scan_date, result)

    def get_all_scan_results(self):
        return self.model.get_all()

    def update_scan_result(self, result_id, profile_id, scan_date, result):
        self.model.update(result_id, profile_id, scan_date, result)

    def delete_scan_result(self, result_id):
        self.model.delete(result_id)
