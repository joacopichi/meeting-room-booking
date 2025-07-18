class BookingValidationStrategy:
    def validate(self, bookings, room, date, duration):
        raise NotImplementedError("Strategy must implement the validate method")
