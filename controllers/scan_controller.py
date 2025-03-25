import nmap
from models.scan_profile_devices_model import ScanProfileDevice
from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities
from models.network_device_model import NetworkDeviceModel
from models.device_scan_model import DeviceScanModel
from config.db_config import get_db_connection
from models.vulnerability_model import VulnerabilityModel
from models.profile_scan_result_model import ProfileScanResultModel
import ipaddress

class ScanController:

    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.device_model = ScanProfileDevice
        self.scan_profile_vulnerabilities_model = ScanProfileVulnerabilities
        self.network_device_model = NetworkDeviceModel
        self.device_scan_model = DeviceScanModel
        self.vulnerabilities_model = VulnerabilityModel
        self.profile_scan_result_model = ProfileScanResultModel()  # Instantiate ProfileScanResultModel

    def scan_profile(self, profile_id):
        ip_addresses = self.device_model.get_ip_address_by_profile_id(self, profile_id)
        cve_ids = self.scan_profile_vulnerabilities_model.get_cve_id_by_profile_id(self, profile_id)

        for ip_address in ip_addresses:
            ip_address = ip_address[0].strip()

            nm = nmap.PortScanner()

            try:
                print("scan started  for ", ip_address)
                nm.scan(ip_address, arguments='-Pn -sV --script=vuln')

                if not nm.all_hosts():
                    continue

                for host in nm.all_hosts():
                    for proto in nm[host].all_protocols():
                        for port in nm[host][proto]:
                            if 'script' in nm[host][proto][port]:
                                for script, output in nm[host][proto][port]['script'].items():
                                    for cve_id in cve_ids:
                                        cve_id = cve_id[0].strip().upper()
                                        if cve_id.startswith("CVE-") and cve_id in output:

                                            # Store the result in ProfileScanResultModel
                                            self.profile_scan_result_model.add_scan_result(
                                                profile_id,
                                                self.network_device_model.get_devices_id_by_ip(self, ip_address)[0],
                                                self.vulnerabilities_model.get_vulnerability_by_cve_id(self, cve_id)[0],
                                                port,
                                                True
                                            )
            except Exception as e:
                pass

    def get_os(self,ip_address):
        """Detect OS of a given IP using Nmap."""
        scanner = nmap.PortScanner()
        os = "Unknown OS"
        try:
            scanner.scan(ip_address, arguments='-O --min-parallelism 10 --max-retries 2')
            if 'osmatch' in scanner[ip_address]:
                os_list = scanner[ip_address]['osmatch']
                if os_list:
                    os = os_list[0]['name']
        except Exception:
            os = "Unknown OS"
        self.network_device_model.update_type(self,ip_address,os)

    def scan_devices_when_adding(self, ip_address):
        self.get_os(ip_address)
        self.scan_vulnerabilities(ip_address)

    def scan_vulnerabilities(self, ip_address):
        nm = nmap.PortScanner()
        print("Scaning ",ip_address)
        nm.scan(ip_address, arguments='-T4 -F --script=vuln')
        if not nm.all_hosts():
            return None

        device_id = self.network_device_model.get_devices_id_by_ip(self,ip_address)[0]
        severity_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}

        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    if 'script' in nm[host][proto][port]:
                        for script, output in nm[host][proto][port]['script'].items():
                            for line in output.split('\n'):
                                if 'CVE:' in line:
                                    cve_id_line = line.split(":")
                                    cve_id = cve_id_line[2].strip()
                                    vulnerability = self.vulnerabilities_model.get_vulnerability_by_cve_id(self,cve_id)
                                    if vulnerability:
                                        severity = float(vulnerability[2])
                                        self.device_scan_model.add_or_update_scan_result(self,device_id, vulnerability[0],port)
                                        if 0 <= severity < 3:
                                            severity_counts['low'] += 1
                                        elif 3 <= severity < 6:
                                            severity_counts['medium'] += 1
                                        elif 6 <= severity < 8:
                                            severity_counts['high'] += 1
                                        elif 8 <= severity <= 10:
                                            severity_counts['critical'] += 1

        self.network_device_model.update_scan_result(self,ip_address, severity_counts)
        print("finished ",ip_address)