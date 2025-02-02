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
                ScanDate DATE NOT NULL,
                CriticalVulnerabilities INT NOT NULL,
                TotalVulnerabilities INT NOT NULL
            );
        """)
        self.conn.commit()

    def add(self, scan_date, critical_vul, total_vul):

        try:
            self.cursor.execute("INSERT INTO ScanResult (ScanDate, CriticalVulnerabilities, TotalVulnerabilities) VALUES (%s, %s, %s)", (scan_date, critical_vul, total_vul))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_all(self):
        self.cursor.execute("SELECT * FROM ScanResult")
        return self.cursor.fetchall()

    def update(self, result_id, scan_date, critical_vul, total_vul):
        self.cursor.execute("UPDATE ScanResult SET ScanDate = %s, CriticalVulnerabilities = %s, TotalVulnerabilities = %s WHERE ResultID = %s", (scan_date, critical_vul, total_vul, result_id))
        self.conn.commit()

    def delete(self, result_id):
        self.cursor.execute("DELETE FROM ScanResult WHERE ResultID = %s", (result_id,))
        self.conn.commit()

