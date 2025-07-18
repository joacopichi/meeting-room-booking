from src.models.User import User

class UserRepository:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def save(self, name, email):
        user = User(self.next_id, name, email)
        self.users.append(user)
        self.next_id += 1
        return user

    def find_all(self):
        return self.users

    def find_by_id(self, user_id):
        return next((u for u in self.users if u.user_id == user_id), None)
