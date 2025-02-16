import bcrypt
from config.db_config import get_db_connection

class UserModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                UserID INT PRIMARY KEY AUTO_INCREMENT,
                UserName VARCHAR(255) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Role VARCHAR(50) NOT NULL
            )
        """)
        self.conn.commit()

    def create_user(self, username, password, role):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.cursor.execute("INSERT INTO users (UserName, Password, Role) VALUES (%s, %s, %s)", (username, hashed_password, role))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def read_users(self):
        self.cursor.execute("SELECT username,role FROM users")
        return self.cursor.fetchall()

    def update_user_role(self, username, role):
        self.cursor.execute("UPDATE users SET Role = %s  WHERE username = %s", (role, username))
        self.conn.commit()

    def update_user_password(self, username, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("UPDATE users SET Password = %s WHERE username = %s", (hashed_password, username))
        self.conn.commit()

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        self.conn.commit()

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = self.cursor.fetchone()

        if user:
            stored_hashed_password = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return_user = (user[0],user[3])
                return return_user

        return None
