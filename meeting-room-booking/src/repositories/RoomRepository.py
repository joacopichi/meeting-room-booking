from src.models.Room import Room

class RoomRepository:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.key = "rooms"
        self.next_id = 1

    def save(self, name, capacity):
        room = Room(self.next_id, name, capacity)
        self.next_id += 1

        if self.redis:
            self.redis.hset(self.key, room.room_id, f"{room.name}|{room.capacity}")
        else:
            if not hasattr(self, "rooms"):
                self.rooms = []
            self.rooms.append(room)

        return room

    def find_all(self):
        if self.redis:
            all_rooms = []
            for rid, value in self.redis.hgetall(self.key).items():
                name, capacity = value.split("|")
                all_rooms.append(Room(int(rid), name, int(capacity)))
            return all_rooms
        else:
            return getattr(self, "rooms", [])

    def find_by_id(self, room_id):
        if self.redis:
            value = self.redis.hget(self.key, room_id)
            if value:
                name, capacity = value.split("|")
                return Room(room_id, name, int(capacity))
            return None
        else:
            return next((r for r in getattr(self, "rooms", []) if r.room_id == room_id), None)
