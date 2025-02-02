from config.db_config import get_db_connection


class ScanProfile:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        profile_table_query = """
        CREATE TABLE IF NOT EXISTS ScanProfile (
            ProfileID INT AUTO_INCREMENT PRIMARY KEY,
            UserID INT NOT NULL,
            ScanFrequency INT NOT NULL,
            FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
        )
        """
        self.cursor.execute(profile_table_query)
        self.conn.commit()

    def create_profile(self, user_id, scan_frequency):
        query = "INSERT INTO ScanProfile (UserID, ScanFrequency) VALUES (%s, %s)"
        self.cursor.execute(query, (user_id, scan_frequency))
        self.conn.commit()

    def read_profiles(self):
        query = "SELECT ProfileID, UserID, ScanFrequency FROM ScanProfile"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def read_profiles_by_id(self,profile_id):
        query = "SELECT ProfileID, UserID, ScanFrequency FROM ScanProfile WHERE ProfileID=%s"
        self.cursor.execute(query, (profile_id,))
        return self.cursor.fetchone()

    def read_profiles_by_user_id(self,user_id):
        query = "SELECT ProfileID, UserID, ScanFrequency FROM ScanProfile WHERE UserID=%s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def update_profile(self, profile_id, user_id, scan_frequency):
        query = "UPDATE ScanProfile SET UserID=%s, ScanFrequency=%s WHERE ProfileID=%s"
        self.cursor.execute(query, (user_id, scan_frequency, profile_id))
        self.conn.commit()

    def delete_profile(self, profile_id):
        query = "DELETE FROM ScanProfile WHERE ProfileID=%s"
        self.cursor.execute(query, (profile_id,))
        self.conn.commit()
