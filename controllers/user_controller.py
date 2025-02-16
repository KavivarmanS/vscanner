import bcrypt
from models.user_model import UserModel

class UserController:
    def __init__(self):
        self.model = UserModel()

    def create_user(self, username, password, role):
        return self.model.create_user(username, password, role)

    def read_users(self):
        return self.model.read_users()

    def update_user_role(self, username, role):
        self.model.update_user_role(username, role)

    def update_user_password(self, username, new_password):
        self.model.update_user_password(username, new_password)

    def delete_user(self, username):
        self.model.delete_user(username)

    def authenticate_user(self, username, password):
        return self.model.authenticate_user(username, password)