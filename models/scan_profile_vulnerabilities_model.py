from config.db_config import get_db_connection

class ScanProfileVulnerabilities:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ScanProfileVulnerabilities ( 
                        ProfileID INT,
                        VulnerabilityID INT,
                        PRIMARY KEY (ProfileID, VulnerabilityID),
                        FOREIGN KEY (ProfileID) REFERENCES ScanProfile(ProfileID) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (VulnerabilityID) REFERENCES Vulnerabilities(VulnerabilityID) ON DELETE CASCADE ON UPDATE CASCADE
                    );
                """)
        self.conn.commit()

    def add(self, profile_id, vulnerability_id):
        query = "INSERT INTO ScanProfileVulnerabilities (ProfileID, VulnerabilityID) VALUES (%s, %s)"

        try:
            self.cursor.execute(query, (profile_id, vulnerability_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


    def get_all(self):
        query = "SELECT * FROM ScanProfileVulnerabilities"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_vulnerabilities_by_profile_id(self,profile_id):
        self.cursor.execute("SELECT v.* FROM ScanProfileVulnerabilities s INNER JOIN Vulnerabilities v ON s.VulnerabilityID = v.VulnerabilityID WHERE s.ProfileID= %s", (profile_id, ))
        return self.cursor.fetchall()

    def get_cve_id_by_profile_id(self,profile_id):
        self.cursor.execute("SELECT v.CVE_ID FROM ScanProfileVulnerabilities s INNER JOIN Vulnerabilities v ON s.VulnerabilityID = v.VulnerabilityID WHERE s.ProfileID= %s", (profile_id, ))
        return self.cursor.fetchall()

    def delete(self, profile_id, vulnerability_id):
        query = "DELETE FROM ScanProfileVulnerabilities WHERE ProfileID = %s AND VulnerabilityID = %s"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (profile_id, vulnerability_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def delete_by_profile_id(self, profile_id):
        query = "DELETE FROM ScanProfileVulnerabilities WHERE ProfileID = %s "
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (profile_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def get_vulnerabilities_count_by_profile_id(self,profile_id):
        self.cursor.execute("SELECT COUNT(s.VulnerabilityID) FROM ScanProfileVulnerabilities s WHERE s.ProfileID= %s", (profile_id, ))
        return self.cursor.fetchall()



