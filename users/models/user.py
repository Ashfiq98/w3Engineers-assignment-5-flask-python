class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password  # This should already be hashed
        self.role = role

    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}', role='{self.role}')"