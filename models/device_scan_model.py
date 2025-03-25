# models/device_scan_model.py
from config.db_config import get_db_connection

class DeviceScanModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.create_table()

    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS DeviceScans (
                    DeviceID INT NOT NULL,
                    VulnerabilityID INT NOT NULL,
                    Port INT NOT NULL,
                    ScanTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (DeviceID, VulnerabilityID, Port),
                    FOREIGN KEY (DeviceID) REFERENCES NetworkDevice(DeviceID),
                    FOREIGN KEY (VulnerabilityID) REFERENCES Vulnerabilities(VulnerabilityID)
                )
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def add_or_update_scan_result(self, device_id, vulnerability_id, port):
        query = """INSERT INTO DeviceScans (DeviceID, VulnerabilityID, Port)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                ScanTimestamp = CURRENT_TIMESTAMP
                """
        cursor = self.conn.cursor()
        cursor.execute(query, (device_id, vulnerability_id, port))
        self.conn.commit()

    def get_scan_results(self):
        query = "SELECT * FROM DeviceScans"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_scan_results_by_device_id(self, device_id):
        query = "SELECT * FROM DeviceScans WHERE DeviceID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (device_id,))
        return cursor.fetchall()

    def delete_scan_results_by_device_id(self, device_id):
        query = "DELETE FROM DeviceScans WHERE DeviceID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (device_id,))
        self.conn.commit()

    def get_scan_details_by_device_id(self, device_id):
        query = """
        SELECT ds.Port, v.CVE_ID, v.Description, ds.ScanTimestamp
        FROM DeviceScans ds
        JOIN Vulnerabilities v ON ds.VulnerabilityID = v.VulnerabilityID
        WHERE ds.DeviceID = %s
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (device_id,))
        return cursor.fetchall()