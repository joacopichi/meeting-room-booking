from src.repositories.BookingRepository import BookingRepository
from src.patterns.BookingValidationStrategy import BookingValidationStrategy

class BookingService:
    def __init__(self, repository: BookingRepository, validation_strategy: BookingValidationStrategy):
        self.repository = repository
        self.validation_strategy = validation_strategy

    def create_booking(self, user, room, date, duration_hours):
        bookings = self.repository.find_all()
        if not self.validation_strategy.validate(bookings, room, date, duration_hours):
            raise Exception("Room is not available at the requested time.")

        return self.repository.save(user, room, date, duration_hours)

    def list_bookings(self):
        return self.repository.find_all()

    def bookings_by_user(self, user_id: int):
        return self.repository.find_by_user(user_id)

    def bookings_by_room(self, room_id: int):
        return self.repository.find_by_room(room_id)
