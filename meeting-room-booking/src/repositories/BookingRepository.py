from src.models.Booking import Booking

class BookingRepository:
    def __init__(self):
        self.bookings = []
        self.next_id = 1

    def save(self, user, room, date, duration_hours):
        booking = Booking(self.next_id, user, room, date, duration_hours)
        self.bookings.append(booking)
        self.next_id += 1
        return booking

    def find_all(self):
        return self.bookings

    def find_by_user(self, user_id):
        return [b for b in self.bookings if b.user.user_id == user_id]

    def find_by_room(self, room_id):
        return [b for b in self.bookings if b.room.room_id == room_id]
