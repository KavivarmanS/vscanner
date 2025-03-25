# controllers/device_scan_controller.py
import threading
import time
from models.device_scan_model import DeviceScanModel

class DeviceScanController:
    def __init__(self, view):
        self.view = view
        self.model = DeviceScanModel()

    def get_scan_details_text(self, device_id):
        scan_details = self.model.get_scan_details_by_device_id(device_id)
        if not scan_details:
            return f"No scan details found for device ID {device_id}."

        details_text = f"Scan details for device ID {device_id}:\n\n"
        for detail in scan_details:
            port, cve_id, description, scan_time = detail
            details_text += (
                f"Port: {port}\n"
                f"CVE ID: {cve_id}\n"
                f"Description: {description}\n"
                f"Scan Time: {scan_time}\n"
                f"{'-'*40}\n"
            )

        return details_text