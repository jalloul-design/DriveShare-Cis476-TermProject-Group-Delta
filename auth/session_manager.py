# Owned By Mira
# Singleton Class goes here, instances, methods like login, logout, get the current user

class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.current_user_logged_in = None
        return cls._instance

    def login(self, user_email):
        self.current_user_logged_in = user_email

    def logout(self):
        self.current_user_logged_in = None

    def get_current_user(self):
        return self.current_user_logged_in

    def user_logged_in(self):
        return self.current_user_logged_in is not None








