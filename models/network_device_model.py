from config.db_config import get_db_connection
import time
import mysql.connector

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
                Low INTEGER,
                Medium INTEGER,
                High INTEGER,
                Critical INTEGER,
                UNIQUE(IPaddress)
            )
        """)
        self.conn.commit()

    def create_device(self, device_name, location, device_type, ip_address):
        query = "INSERT INTO NetworkDevice (DeviceName, Location, Type, IPAddress) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (device_name, location, device_type, ip_address))
        self.conn.commit()

    def read_devices(self):
        query = "SELECT DeviceID,DeviceName, Location, Type, IPAddress FROM NetworkDevice"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_devices_by_id(self,device_id):
        query = "SELECT DeviceID, DeviceName, Location, Type, IPAddress FROM NetworkDevice WHERE DeviceID=%s"
        self.cursor.execute(query, (device_id,))
        return self.cursor.fetchone()

    def get_devices_id_by_ip(self,ip_address):
        query = "SELECT DeviceID FROM NetworkDevice WHERE IPAddress=%s"
        self.cursor.execute(query, (ip_address,))
        return self.cursor.fetchone()

    def get_devices_ip_by_id(self,device_id):
        query = "SELECT IPAddress FROM NetworkDevice WHERE DeviceID=%s"
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

    def read_devices_for_profile_add(self, profile_id):
        query = "SELECT DeviceID,DeviceName, Location, Type, IPAddress FROM NetworkDevice WHERE DeviceID NOT IN (SELECT DeviceID FROM ScanProfileDevices WHERE ProfileID = %s) "
        self.cursor.execute(query,(profile_id,))
        return self.cursor.fetchall()

    def check_device_by_ip(self,ip_address):
        query = "SELECT 1 FROM NetworkDevice WHERE IPAddress=%s LIMIT 1"
        self.cursor.execute(query, (ip_address,))
        result = self.cursor.fetchone()
        return result is not None

    def get_last_device(self):
        query = "SELECT DeviceID FROM NetworkDevice ORDER BY DeviceID DESC LIMIT 1"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def update_scan_result(self, ip_address, severity_counts):
        query = "UPDATE NetworkDevice SET Low=%s, Medium=%s, High=%s, Critical=%s WHERE IPaddress=%s"
        self.cursor.execute(query, (severity_counts['low'], severity_counts['medium'], severity_counts['high'], severity_counts['critical'], ip_address))
        self.conn.commit()

    def update_type(self, ip_address, type):
        query = "UPDATE NetworkDevice SET Type=%s WHERE IPaddress=%s"
        retries = 3
        for attempt in range(retries):
            try:
                self.cursor.execute(query, (type, ip_address))
                self.conn.commit()
                break
            except mysql.connector.errors.OperationalError as e:
                if attempt < retries - 1:
                    time.sleep(2)  # Wait for 2 seconds before retrying
                    self.conn = get_db_connection()  # Reconnect to the database
                    self.cursor = self.conn.cursor()
                else:
                    raise e

    def get_scan_result_by_device_id(self,device_id):
        query = "SELECT Low, Medium, High, Critical FROM NetworkDevice WHERE DeviceID=%s"
        self.cursor.execute(query, (device_id,))
        return self.cursor.fetchone()
