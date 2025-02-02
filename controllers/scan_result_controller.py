from models.scan_result_model import ScanResultModel
from datetime import date

class ScanResultController:
    def __init__(self):
        self.model = ScanResultModel()

    def add_scan_result(self, critical_vul, total_vul):
        scan_date = date.today()
        return self.model.add(scan_date, critical_vul, total_vul)

    def get_all_scan_results(self):
        return self.model.get_all()

    def update_scan_result(self, result_id, scan_date, critical_vul, total_vul):
        self.model.update(result_id, scan_date, critical_vul, total_vul)

    def delete_scan_result(self, result_id):
        self.model.delete(result_id)
