import scapy.all as scapy
import e
import nmap
import geocoder
from models.network_device_model import NetworkDeviceModel
from controllers.scan_controller import ScanController
from tkinter import simpledialog, messagebox
import time
import threading
from scapy.all import (ARP, Ether, srp)
import ipaddress
import socket
import netifaces



class NetworkDeviceController:
    def __init__(self, view):
        self.model = NetworkDeviceModel()
        self.view = view
        self.scan = ScanController()

    def add_device(self, device_name, location, device_type, ip_address):
        """Add a new device to the database."""
        self.model.create_device(device_name, location, device_type, ip_address)

    def get_devices(self):
        return self.model.read_devices()

    def get_devices_by_id(self, device_id):
        return self.model.get_devices_by_id(device_id)

    def get_devices_id_by_ip(self, ip_address):
        return self.model.get_devices_id_by_ip(ip_address)

    def get_devices_for_profile_add(self, profile_id):
        return self.model.read_devices_for_profile_add(profile_id)

    def get_scan_result_by_device_id(self, device_id):
        result = self.model.get_scan_result_by_device_id(device_id)
        if result:
            severity_counts = {
                'low': result[0],
                'medium': result[1],
                'high': result[2],
                'critical': result[3]
            }
        else:
            severity_counts = None
        return severity_counts

    def modify_device(self, device_id, device_name, location, device_type, ip_address):
        self.model.update_device(device_id, device_name, location, device_type, ip_address)

    def remove_device(self, device_id):
        self.model.delete_device(device_id)



    def scan_and_add_devices(self):
        print("scan_and_add_devices")
        try:
            network_address = self.get_current_network_address()
            if not network_address:
                self.view.parent.after(0, lambda: messagebox.showerror("Error", "No active network interfaces detected."))
                return

            g = geocoder.ip('me')
            current_location = g.city if g.city else "City not found"

            devices = self.get_connected_devices(network_address)
            if not devices:
                self.view.parent.after(0, lambda: messagebox.showinfo("Info", "No devices found on the network."))
                return


            devices_found = len(devices)
            devices_added = 0

            # Get the last device ID from the database
            last_device = self.model.get_last_device()
            last_device_id = last_device[0] if last_device else 0

            for device_ip in devices:
                if not self.model.check_device_by_ip(device_ip):
                    last_device_id += 1
                    device_name = f"PC{last_device_id}"
                    self.add_device(device_name, current_location, "Scanning", device_ip)  # OS type is set to None

                    devices_added += 1
                    threading.Thread(target=self.scan.scan_devices_when_adding, args=(device_ip,)).start()

            self.view.parent.after(0, lambda: messagebox.showinfo("Success", f"Added {devices_added} devices successfully!"))
        except Exception as e:
            self.view.parent.after(0, lambda e=e: messagebox.showerror("Error", f"Error scanning network: {e}"))

    def get_current_network_address(self):
        print("get_current_network_address")
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                for address in addresses[netifaces.AF_INET]:
                    if address['addr'] == ip_address:
                        netmask = address['netmask']
                        network = ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)
                        print(network)
                        return str(network)
        return None

    def get_connected_devices(self,network):
        devices = set()

        # Create an ARP request packet
        arp_request = ARP(pdst=network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request

        # Send the packet and get responses
        answered, _ = srp(packet, timeout=2, verbose=False)

        for sent, received in answered:
            devices.add(received.psrc)  # Store unique IP addresses

        return list(devices)