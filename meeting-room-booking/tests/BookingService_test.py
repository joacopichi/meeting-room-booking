import unittest
from datetime import datetime, timedelta
from src.models.User import User
from src.models.Room import Room
from src.repositories.BookingRepository import BookingRepository
from src.patterns.DefaultValidation import DefaultValidation
from src.services.BookingService import BookingService

class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.repo = BookingRepository()
        self.validation = DefaultValidation()
        self.service = BookingService(self.repo, self.validation)

        self.user = User(1, "Test User", "test@example.com")
        self.room = Room(1, "Conference Room", 10)

    def test_create_booking_success(self):
        date = datetime.now()
        booking = self.service.create_booking(self.user, self.room, date, 2)
        self.assertIsNotNone(booking)
        self.assertEqual(len(self.repo.find_all()), 1)

    def test_create_booking_overlap_fails(self):
        date = datetime.now()
        self.service.create_booking(self.user, self.room, date, 2)
        with self.assertRaises(Exception):
            self.service.create_booking(self.user, self.room, date + timedelta(minutes=30), 1)

if __name__ == '__main__':
    unittest.main()