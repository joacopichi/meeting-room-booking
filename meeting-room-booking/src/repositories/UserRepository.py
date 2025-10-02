from src.models.User import User

class UserRepository:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.key = "users"
        self.next_id = 1

    def save(self, name, email):
        user = User(self.next_id, name, email)
        self.next_id += 1

        if self.redis:
            self.redis.hset(self.key, user.user_id, f"{user.name}|{user.email}")
        else:
            if not hasattr(self, "users"):
                self.users = []
            self.users.append(user)

        return user

    def find_all(self):
        if self.redis:
            all_users = []
            for uid, value in self.redis.hgetall(self.key).items():
                name, email = value.split("|")
                all_users.append(User(int(uid), name, email))
            return all_users
        else:
            return getattr(self, "users", [])

    def find_by_id(self, user_id):
        if self.redis:
            value = self.redis.hget(self.key, user_id)
            if value:
                name, email = value.split("|")
                return User(user_id, name, email)
            return None
        else:
            return next((u for u in getattr(self, "users", []) if u.user_id == user_id), None)
