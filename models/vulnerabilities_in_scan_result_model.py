from config.db_config import get_db_connection

class VulnerabilitiesInScanResultModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS VulnerabilitiesInScanResult (
                        ResultID INT,
                        VulnerabilityID INT,
                        PRIMARY KEY (ResultID, VulnerabilityID),
                        FOREIGN KEY (ResultID) REFERENCES ScanResult(ResultID),
                        FOREIGN KEY (VulnerabilityID) REFERENCES vulnerabilities(VulnerabilityID)
                    );
                """)
        self.conn.commit()

    def add(self, result_id, vulnerability_id):
        try:
            self.cursor.execute("INSERT INTO VulnerabilitiesInScanResult (ResultID, VulnerabilityID) VALUES (%s, %s)", (result_id, vulnerability_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


    def get_all(self):
        self.cursor.execute("SELECT * FROM VulnerabilitiesInScanResult")
        return self.cursor.fetchall()

    def delete(self, result_id, vulnerability_id):
        try:
            self.cursor.execute("DELETE FROM VulnerabilitiesInScanResult WHERE ResultID = %s AND VulnerabilityID = %s", (result_id, vulnerability_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

