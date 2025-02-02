from models.network_device_model import NetworkDeviceModel

class NetworkDeviceController:
    def __init__(self):
        self.model = NetworkDeviceModel()

    def add_device(self, device_name, location, device_type, ip_address):
        self.model.create_device(device_name, location, device_type, ip_address)

    def get_devices(self):
        return self.model.read_devices()

    def get_devices_by_id(self,device_id):
        return self.model.get_devices_by_id(device_id)

    def modify_device(self, device_id, device_name, location, device_type, ip_address):
        self.model.update_device(device_id, device_name, location, device_type, ip_address)

    def remove_device(self, device_id):
        self.model.delete_device(device_id)
