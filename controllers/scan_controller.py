import nmap
from fpdf import FPDF
from models.scan_profile_devices_model import ScanProfileDevice
from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities
from config.db_config import get_db_connection

class ScanController:

    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()


    def scan_for_cve(self, profile_id, output_pdf="scan_results.pdf"):

        ip_addresses = ScanProfileDevice.get_ip_address_by_profile_id(self, profile_id)
        cve_ids = ScanProfileVulnerabilities.get_cve_id_by_profile_id(self, profile_id)

        nm = nmap.PortScanner()
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)

        # Title
        pdf.cell(200, 10, "Vulnerability Scan Report", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, f"Scanning the following IPs: {', '.join(ip_addresses)}", ln=True)
        pdf.cell(200, 10, f"Checking for CVEs: {', '.join(cve_ids)}", ln=True)
        pdf.ln(10)

        for ip_address in ip_addresses:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, f"Scanning {ip_address}...", ln=True)
            pdf.ln(5)

            try:
                nm.scan(ip_address, arguments='-Pn -sV --script=vulners')

                if not nm.all_hosts():
                    pdf.set_font("Arial", "I", 12)
                    pdf.cell(200, 10, f"No hosts found at {ip_address}.", ln=True)
                    pdf.ln(10)
                    continue

                for host in nm.all_hosts():
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(200, 10, f"Host: {host} ({nm[host].hostname()})", ln=True)
                    pdf.cell(200, 10, f"State: {nm[host].state()}", ln=True)
                    pdf.ln(5)

                    for proto in nm[host].all_protocols():
                        pdf.set_font("Arial", "B", 12)
                        pdf.cell(200, 10, f"Protocol: {proto}", ln=True)

                        lport = nm[host][proto].keys()
                        for port in lport:
                            pdf.set_font("Arial", size=12)
                            pdf.cell(200, 10, f"Port: {port} - State: {nm[host][proto][port]['state']}", ln=True)

                            if 'script' in nm[host][proto][port]:
                                for script, output in nm[host][proto][port]['script'].items():
                                    detected_cves = [cve for cve in cve_ids if cve in output]
                                    if detected_cves:
                                        pdf.set_text_color(255, 0, 0)  # Red for vulnerabilities
                                        pdf.multi_cell(0, 10,
                                                       f"[!] CVEs detected on port {port}: {', '.join(detected_cves)}",
                                                       border=1)
                                        pdf.set_text_color(0, 0, 0)  # Reset color
                                        pdf.multi_cell(0, 10, f"Details: {output}")
                                        pdf.ln(5)
                            else:
                                pdf.cell(200, 10, f"No vulnerabilities detected on port {port}.", ln=True)

                        pdf.ln(5)

            except Exception as e:
                pdf.set_text_color(255, 0, 0)
                pdf.cell(200, 10, f"An error occurred while scanning {ip_address}: {e}", ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(10)

        pdf.output(output_pdf)
        print(f"Scan results saved as {output_pdf}")
