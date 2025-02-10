import json
import os

class Session:
    _instance = None
    SESSION_FILE = "session.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.user_id = None
            cls._instance.role = None
            cls._instance.load_session()
        return cls._instance

    def set_user(self, user_id, role, remember=False):
        self.user_id = user_id
        self.role = role
        if remember:
            self.save_session()

    def get_user(self):
        return self.user_id, self.role

    def get_role(self):
        return self.role

    def save_session(self):
        with open(self.SESSION_FILE, "w") as file:
            json.dump({"user_id": self.user_id, "role": self.role}, file)

    def load_session(self):
        if os.path.exists(self.SESSION_FILE):
            try:
                with open(self.SESSION_FILE, "r") as file:
                    data = json.load(file)
                    self.user_id = data.get("user_id")
                    self.role = data.get("role")
            except json.JSONDecodeError:
                self.user_id = None
                self.role = None

    def clear_session(self):
        self.user_id = None
        self.role = None
        if os.path.exists(self.SESSION_FILE):
            os.remove(self.SESSION_FILE)
