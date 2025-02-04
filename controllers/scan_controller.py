import nmap
from models.scan_profile_devices_model import ScanProfileDevice
from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities
from config.db_config import get_db_connection

class ScanController:

    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.devide_model = ScanProfileDevice
        self.vulnerabilities_model = ScanProfileVulnerabilities

    def scan_for_cves(self,profile_id):
        ip_addresses = self.devide_model.get_ip_address_by_profile_id(self,profile_id)
        cve_ids = self.vulnerabilities_model.get_cve_id_by_profile_id(self,profile_id)
        result_str = ""

        for ip_address in ip_addresses:
            print(ip_address)
            ip_address = ip_address[0].strip()

            nm = nmap.PortScanner()
            result_str += f"\nScanning {ip_address} for vulnerabilities...\n"

            cve_found = False

            try:
                nm.scan(ip_address, arguments='-Pn -sV --script=vuln')

                if not nm.all_hosts():
                    result_str += f"No hosts found at {ip_address}.\n"
                    continue

                for host in nm.all_hosts():
                    result_str += f"\nHost: {host} ({nm[host].hostname()})\n"
                    result_str += f"State: {nm[host].state()}\n"

                    for proto in nm[host].all_protocols():
                        result_str += f"Protocol: {proto}\n"

                        for port in nm[host][proto]:
                            state = nm[host][proto][port]['state']
                            result_str += f"Port: {port} - State: {state}\n"

                            if 'script' in nm[host][proto][port]:
                                for script, output in nm[host][proto][port]['script'].items():
                                    for cve_id in cve_ids:
                                        cve_id = cve_id[0].strip().upper()
                                        if cve_id.startswith("CVE-") and cve_id in output:
                                            result_str += f"[!] CVE {cve_id} detected on port {port}!\n"
                                            result_str += f"Details: {output}\n"
                                            cve_found = True

                if not cve_found:
                    result_str += f"[+] No specified CVEs detected on {ip_address}.\n"

            except Exception as e:
                result_str += f"An error occurred while scanning {ip_address}: {e}\n"

        return result_str