from config.db_config import get_db_connection

class ScanResultModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ScanResult (
                ResultID INT PRIMARY KEY AUTO_INCREMENT,
                ProfileID INT,
                ScanDate DATE NOT NULL,
                Result VARCHAR(50000) NOT NULL,
                FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID) ON DELETE CASCADE ON UPDATE CASCADE
            );
        """)
        self.conn.commit()

    def add(self, profile_id, scan_date, result):

        try:
            self.cursor.execute("INSERT INTO ScanResult (ProfileID, ScanDate, Result) VALUES (%s, %s, %s)", (profile_id, scan_date, result))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_all(self):
        self.cursor.execute("SELECT * FROM ScanResult")
        return self.cursor.fetchall()

    def update(self, result_id, profile_id, scan_date, result):
        self.cursor.execute("UPDATE ScanResult SET ProfileID = %s, ScanDate = %s, Result = %s WHERE ResultID = %s", (profile_id, scan_date, result, result_id))
        self.conn.commit()

    def delete(self, result_id):
        self.cursor.execute("DELETE FROM ScanResult WHERE ResultID = %s", (result_id,))
        self.conn.commit()

