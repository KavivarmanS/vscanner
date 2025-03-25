# models/profile_scan_result_model.py
from config.db_config import get_db_connection

class ProfileScanResultModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.create_table()

    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS ProfileScanResult (
                    ProfileID INT NOT NULL,
                    DeviceID INT NOT NULL,
                    VulnerabilityID INT NOT NULL,
                    Port INT NOT NULL,
                    ScanTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    Results BOOLEAN NOT NULL,
                    PRIMARY KEY (ProfileID, DeviceID, VulnerabilityID, Port, ScanTimestamp),
                    FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID),
                    FOREIGN KEY (DeviceID) REFERENCES NetworkDevice(DeviceID),
                    FOREIGN KEY (VulnerabilityID) REFERENCES Vulnerabilities(VulnerabilityID)
                )
                """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def add_scan_result(self, profile_id, device_id, vulnerability_id, port, results):
        query = """INSERT INTO ProfileScanResult (ProfileID, DeviceID, VulnerabilityID, Port, Results)
                VALUES (%s, %s, %s, %s, %s)
                """
        cursor = self.conn.cursor()
        cursor.execute(query, (profile_id, device_id, vulnerability_id, port, results))
        self.conn.commit()

    def get_scan_results(self):
        query = "SELECT * FROM ProfileScanResult"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_scan_results_for_table(self):
        query = "SELECT DISTINCT ProfileID,ScanTimestamp FROM ProfileScanResult"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_scan_results_by_profile_id(self, profile_id):
        query = "SELECT * FROM ProfileScanResult WHERE ProfileID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (profile_id,))
        return cursor.fetchall()

    def delete_scan_result(self, profile_id, device_id, vulnerability_id, port, scan_timestamp):
        query = "DELETE FROM ProfileScanResult WHERE ProfileID = %s AND DeviceID = %s AND VulnerabilityID = %s AND Port = %s AND ScanTimestamp = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (profile_id, device_id, vulnerability_id, port, scan_timestamp))
        self.conn.commit()

    def get_data_for_chart(self, profile_id, scan_timestamp):
        query = "SELECT DeviceID,Port,count(VulnerabilityID) FROM ProfileScanResult WHERE ProfileID = %s and ScanTimestamp = %s GROUP BY DeviceID,Port"
        cursor = self.conn.cursor()
        cursor.execute(query, (profile_id, scan_timestamp))
        return cursor.fetchall()

    def get_vulnerabilities_detected(self,profile_id, scan_timestamp, device_id):
        query = "SELECT p.DeviceID, p.Port, p.VulnerabilityID, v.CVE_ID, v.SeverityLevel, v.SeverityLevel FROM vulnerabilities v INNER JOIN profilescanresult p ON v.VulnerabilityID = p.VulnerabilityID WHERE ProfileID = %s and ScanTimestamp = %s and p.DeviceID = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (profile_id, scan_timestamp, device_id))
        return cursor.fetchall()

