from src.repositories.RoomRepository import RoomRepository

class RoomService:
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def create_room(self, name: str, capacity: int):
        return self.repository.save(name, capacity)

    def list_rooms(self):
        return self.repository.find_all()

    def get_room_by_id(self, room_id: int):
        return self.repository.find_by_id(room_id)
