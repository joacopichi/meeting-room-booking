from src.repositories.UserRepository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, name: str, email: str):
        return self.repository.save(name, email)

    def list_users(self):
        return self.repository.find_all()

    def get_user_by_id(self, user_id: int):
        return self.repository.find_by_id(user_id)