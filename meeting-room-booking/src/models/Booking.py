from datetime import datetime

class Booking:
    def __init__(self, booking_id: int, user, room, date: datetime, duration_hours: int):
        self.booking_id = booking_id
        self.user = user
        self.room = room
        self.date = date
        self.duration_hours = duration_hours

    def __str__(self):
        return f"Booking({self.booking_id}) - User: {self.user.name}, Room: {self.room.name}, Date: {self.date}, Duration: {self.duration_hours}h"
