import socket
import scapy.all as scapy
import nmap
import netifaces
import geocoder
from models.network_device_model import NetworkDeviceModel
from tkinter import simpledialog, messagebox


class NetworkDeviceController:
    def __init__(self, view):
        self.model = NetworkDeviceModel()
        self.view = view

    def add_device(self, device_name, location, device_type, ip_address):
        """Add a new device to the database."""
        self.model.create_device(device_name, location, device_type, ip_address)
        self.view.load_data()

    def get_devices(self):
        return self.model.read_devices()

    def get_devices_by_id(self, device_id):
        return self.model.get_devices_by_id(device_id)

    def modify_device(self, device_id, device_name, location, device_type, ip_address):
        self.model.update_device(device_id, device_name, location, device_type, ip_address)

    def remove_device(self, device_id):
        self.model.delete_device(device_id)

    def get_all_network_ranges(self):
        """Get network ranges for all active interfaces (Wi-Fi, Ethernet, etc.)."""
        network_ranges = []
        interfaces = netifaces.interfaces()

        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    subnet = ".".join(ip.split(".")[:3]) + ".0/24"
                    network_ranges.append(subnet)

        return list(set(network_ranges))  # Remove duplicates

    def fast_scan(self, ip_range):
        """Perform fast ARP scan to find active devices."""
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        devices = []
        for sent, received in answered_list:
            devices.append({'ip': received.psrc})

        return devices

    def get_os(self, ip):
        """Detect OS of a given IP using Nmap."""
        scanner = nmap.PortScanner()
        try:
            scanner.scan(ip, arguments='-O --min-parallelism 10 --max-retries 2')
            if 'osmatch' in scanner[ip]:
                os_list = scanner[ip]['osmatch']
                if os_list:
                    return os_list[0]['name']
        except Exception:
            return "Unknown OS"
        return "Unknown OS"

    def scan_and_add_devices(self):
        """Scan network, ask for device names, and add to database."""
        network_ranges = self.get_all_network_ranges()
        if not network_ranges:
            messagebox.showerror("Error", "No active network interfaces detected.")
            return

        g = geocoder.ip('me')  # Get location based on public IP
        if g.city:
            current_location =  g.city
        else:
            current_location = "City not found"

        self.view.show_scan_progress("Scanning network for devices...")

        all_devices = []
        for network_range in network_ranges:
            devices = self.fast_scan(network_range)

            for device in devices:
                device_name = simpledialog.askstring("Device Name", f"Enter name for device {device['ip']}:")
                if not device_name:
                    continue

                os_type = self.get_os(device['ip'])
                self.add_device(device_name, current_location, os_type, device['ip'])

                all_devices.append((device_name, device['ip'], os_type))

        self.view.show_scan_progress("Scanning completed!")
        messagebox.showinfo("Success", f"Added {len(all_devices)} devices successfully!")
