class Room:
    def __init__(self, room_id: int, name: str, capacity: int):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return f"Room({self.room_id}): {self.name} - Capacity: {self.capacity}"
