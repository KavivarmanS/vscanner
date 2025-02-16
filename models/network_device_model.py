from config.db_config import get_db_connection

class NetworkDeviceModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS NetworkDevice (
                DeviceID INT PRIMARY KEY AUTO_INCREMENT,
                DeviceName VARCHAR(255) NOT NULL,
                Location VARCHAR(255) NOT NULL,
                Type VARCHAR(50) NOT NULL,
                IPaddress VARCHAR(15) NOT NULL,
                UNIQUE(IPaddress)
            )
        """)
        self.conn.commit()

    def create_device(self, device_name, location, device_type, ip_address):
        query = "INSERT INTO NetworkDevice (DeviceName, Location, Type, IPAddress) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (device_name, location, device_type, ip_address))
        self.conn.commit()

    def read_devices(self):
        query = "SELECT * FROM NetworkDevice"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_devices_by_id(self,device_id):
        query = "SELECT * FROM NetworkDevice WHERE DeviceID=%s"
        self.cursor.execute(query, (device_id,))
        return self.cursor.fetchone()

    def update_device(self, device_id, device_name, location, device_type, ip_address):
        query = "UPDATE NetworkDevice SET DeviceName=%s, Location=%s, Type=%s, IPAddress=%s WHERE DeviceID=%s"
        self.cursor.execute(query, (device_name, location, device_type, ip_address, device_id))
        self.conn.commit()

    def delete_device(self, device_id):
        query = "DELETE FROM NetworkDevice WHERE DeviceID=%s"
        self.cursor.execute(query, (device_id,))
        self.conn.commit()
