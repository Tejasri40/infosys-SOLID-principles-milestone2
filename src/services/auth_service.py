from src.interfaces.auth_interface import AuthInterface
from auth import login_user, add_user

class AuthService(AuthInterface):
    def login(self, username, password):
        return login_user(username, password)

    def register(self, username, password):
        return add_user(username, password)
