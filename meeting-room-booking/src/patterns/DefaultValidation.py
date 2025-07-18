from datetime import timedelta
from src.patterns.BookingValidationStrategy import BookingValidationStrategy

class DefaultValidation(BookingValidationStrategy):
    def validate(self, bookings, room, date, duration):
        end = date + timedelta(hours=duration)
        for b in bookings:
            if b.room.room_id == room.room_id:
                b_end = b.date + timedelta(hours=b.duration_hours)
                if date < b_end and end > b.date:
                    return False
        return True
