from models.profile_scan_result_model import ProfileScanResultModel
from datetime import date
from controllers.scan_controller import ScanController
from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities
from models.scan_profile_devices_model import ScanProfileDevice

class ScanResultController:
    def __init__(self):
        self.model = ProfileScanResultModel()
        self.vulnerabilities_model =ScanProfileVulnerabilities()
        self.devices_model = ScanProfileDevice()

    def add_scan_result(self, profile_id, device_id, vulnerability_id, port, results):
        return self.model.add_scan_result(profile_id, device_id, vulnerability_id, port, results)

    def get_all_scan_results(self):
        return self.model.get_scan_results()

    def get_scan_results_for_table(self):
        return self.model.get_scan_results_for_table()

    def update_scan_result(self, profile_id, device_id, vulnerability_id, port, scan_timestamp, results):
        self.model.delete_scan_result(profile_id, device_id, vulnerability_id, port, scan_timestamp)
        self.model.add_scan_result(profile_id, device_id, vulnerability_id, port, results)

    def delete_scan_result(self, profile_id, device_id, vulnerability_id, port, scan_timestamp):
        self.model.delete_scan_result(profile_id, device_id, vulnerability_id, port, scan_timestamp)


    def get_data_for_chart(self, profile_id, scan_timestamp):
        return self.model.get_data_for_chart(profile_id, scan_timestamp)

    def get_vulnerabilities_detected(self, profile_id, scan_timestamp):
        devices = self.devices_model.get_device_by_profile_id(profile_id)
        vulnerabilities = self.vulnerabilities_model.get_vulnerabilities_by_profile_id(profile_id)
        detected_vulnerabilities = {}

        for device in devices:
            device_id = device[0]
            detected_vulnerabilities[device_id] = self.model.get_vulnerabilities_detected(profile_id, scan_timestamp,
                                                                                          device_id)

        output_text = ""
        for device in devices:
            device_id = device[0]
            device_name = device[1]  # Assuming the device dictionary has a 'DeviceName' key
            ip_address = device[4]
            type = device[3]
            output_text += f"Device: {device_name} (ID: {device_id}, IP address: {ip_address}, Type: {type})\n"
            device_detected_vulns = detected_vulnerabilities[device_id]

            for vulnerability in vulnerabilities:
                vuln_id = vulnerability[0]
                cve_id = vulnerability[1]
                severity = vulnerability[2]
                discription = vulnerability[3]
                if any(dv[2] == vuln_id for dv in device_detected_vulns):
                    output_text += f"  - Detected: {cve_id} (Severity: {severity} out of 10)\n"
                    output_text += f"  \t {discription} \n"
                else:
                    output_text += f"  - Not Detected: {cve_id} (Severity: {severity} out of 10)\n"
                    output_text += f"  \t {discription} \n"
            output_text += "\n"

        return output_text



