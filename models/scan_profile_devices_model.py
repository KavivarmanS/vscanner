from config.db_config import get_db_connection

class ScanProfileDevice:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ScanProfileDevices (
                ProfileID INT,
                DeviceID INT,
                PRIMARY KEY (ProfileID, DeviceID),
                FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID),
                FOREIGN KEY (DeviceID) REFERENCES NetworkDevice(DeviceID)
            );
        """)
        self.conn.commit()

    def add(self, profile_id, device_id):
        try:
            self.cursor.execute("INSERT INTO ScanProfileDevices (ProfileID, DeviceID) VALUES (%s, %s)", (profile_id, device_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_all(self):
        self.cursor.execute("SELECT * FROM ScanProfileDevices")
        return self.cursor.fetchall()

    def get_device_by_profile_id(self,profile_id):
        self.cursor.execute("SELECT n.* FROM ScanProfileDevices s INNER JOIN NetworkDevice n ON s.DeviceID = n.DeviceID WHERE s.ProfileID= %s", (profile_id, ))
        return self.cursor.fetchall()

    def get_ip_address_by_profile_id(self,profile_id):
        self.cursor.execute("SELECT n.IPaddress FROM ScanProfileDevices s INNER JOIN NetworkDevice n ON s.DeviceID = n.DeviceID WHERE s.ProfileID= %s", (profile_id, ))
        return self.cursor.fetchall()

    def delete(self, profile_id, device_id):
        self.cursor.execute("DELETE FROM ScanProfileDevices WHERE ProfileID = %s AND DeviceID = %s", (profile_id, device_id))
        self.conn.commit()


