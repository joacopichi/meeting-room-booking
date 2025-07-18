from src.models.Room import Room

class RoomRepository:
    def __init__(self):
        self.rooms = []
        self.next_id = 1

    def save(self, name, capacity):
        room = Room(self.next_id, name, capacity)
        self.rooms.append(room)
        self.next_id += 1
        return room

    def find_all(self):
        return self.rooms

    def find_by_id(self, room_id):
        return next((r for r in self.rooms if r.room_id == room_id), None)
