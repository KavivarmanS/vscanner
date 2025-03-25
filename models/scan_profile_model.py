from config.db_config import get_db_connection
from models.scan_profile_devices_model import ScanProfileDevice
from models.scan_profile_vulnerabilities_model import ScanProfileVulnerabilities

# models/scan_profile_model.py
class ScanProfile:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.scan_profile_devices_model = ScanProfileDevice
        self.scan_profile_vulnerabilities_model = ScanProfileVulnerabilities
        self.create_table()
    def create_table(self):
        profile_table_query = """
        CREATE TABLE IF NOT EXISTS ScanProfile (
            ProfileID INT AUTO_INCREMENT PRIMARY KEY,
            UserID INT NOT NULL,
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        )
        """
        self.cursor.execute(profile_table_query)
        self.conn.commit()

    def create_profile(self, user_id):
        query = "INSERT INTO ScanProfile (UserID) VALUES (%s)"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def read_profiles(self):
        query = "SELECT ProfileID, UserID FROM ScanProfile"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def read_profiles_by_id(self, profile_id):
        query = "SELECT ProfileID, UserID FROM ScanProfile WHERE ProfileID=%s"
        self.cursor.execute(query, (profile_id,))
        return self.cursor.fetchone()

    def read_profiles_by_user_id(self, user_id):
        query = "SELECT ProfileID, UserID FROM ScanProfile WHERE UserID=%s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def update_profile(self, profile_id, user_id):
        query = "UPDATE ScanProfile SET UserID=%s WHERE ProfileID=%s"
        self.cursor.execute(query, (user_id, profile_id))
        self.conn.commit()

    def delete_profile(self, profile_id):
        self.scan_profile_vulnerabilities_model.delete_by_profile_id(self,profile_id)
        self.scan_profile_devices_model.delete_by_profile_id(self,profile_id)
        query = "DELETE FROM ScanProfile WHERE ProfileID=%s"
        self.cursor.execute(query, (profile_id,))
        self.conn.commit()