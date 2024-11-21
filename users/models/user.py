# models/user.py
class User:
    def __init__(self, name, email, password, role='User'):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
