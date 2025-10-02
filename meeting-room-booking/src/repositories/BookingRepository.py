from src.models.Booking import Booking
from datetime import datetime

class BookingRepository:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.key = "bookings"
        self.next_id = 1

    def save(self, user_id, room_id, start, duration):
        booking = Booking(self.next_id, user_id, room_id, start, duration)
        self.next_id += 1

        if self.redis:
            self.redis.hset(self.key, booking.booking_id,
                            f"{booking.user_id}|{booking.room_id}|{booking.start.isoformat()}|{booking.duration}")
        else:
            if not hasattr(self, "bookings"):
                self.bookings = []
            self.bookings.append(booking)

        return booking

    def find_all(self):
        if self.redis:
            all_bookings = []
            for bid, value in self.redis.hgetall(self.key).items():
                user_id, room_id, start_iso, duration = value.split("|")
                all_bookings.append(
                    Booking(int(bid), int(user_id), int(room_id),
                            datetime.fromisoformat(start_iso), int(duration))
                )
            return all_bookings
        else:
            return getattr(self, "bookings", [])

    def find_by_id(self, booking_id):
        if self.redis:
            value = self.redis.hget(self.key, booking_id)
            if value:
                user_id, room_id, start_iso, duration = value.split("|")
                return Booking(int(booking_id), int(user_id), int(room_id),
                               datetime.fromisoformat(start_iso), int(duration))
            return None
        else:
            return next((b for b in getattr(self, "bookings", []) if b.booking_id == booking_id), None)
