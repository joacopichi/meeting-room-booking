from src.services.UserService import UserService
from src.services.RoomService import RoomService
from src.services.BookingService import BookingService
from src.repositories.UserRepository import UserRepository
from src.repositories.RoomRepository import RoomRepository
from src.repositories.BookingRepository import BookingRepository
from src.patterns.DefaultValidation import DefaultValidation
from datetime import datetime

def print_menu():
    print("\n--- Menu ---")
    print("1. Create user")
    print("2. List users")
    print("3. Create room")
    print("4. List rooms")
    print("5. Create booking")
    print("6. List bookings")
    print("7. Exit")

def main():
    user_service = UserService(UserRepository())
    room_service = RoomService(RoomRepository())
    booking_service = BookingService(BookingRepository(), DefaultValidation())

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("User name: ")
            email = input("User email: ")
            user = user_service.create_user(name, email)
            print(f"User created: {user}")

        elif choice == "2":
            users = user_service.list_users()
            if not users:
                print("No users found.")
            for user in users:
                print(user)

        elif choice == "3":
            name = input("Room name: ")
            try:
                capacity = int(input("Room capacity: "))
            except ValueError:
                print("Invalid capacity.")
                continue
            room = room_service.create_room(name, capacity)
            print(f"Room created: {room}")

        elif choice == "4":
            rooms = room_service.list_rooms()
            if not rooms:
                print("No rooms found.")
            for room in rooms:
                print(room)

        elif choice == "5":
            users = user_service.list_users()
            rooms = room_service.list_rooms()
            if not users or not rooms:
                print("There must be at least one user and one room to create a booking.")
                continue

            print("Users:")
            for user in users:
                print(f"{user.user_id}: {user.name}")
            try:
                user_id = int(input("Enter user ID: "))
                user = user_service.get_user_by_id(user_id)
                if not user:
                    raise ValueError()
            except ValueError:
                print("Invalid or unknown user ID.")
                continue

            print("Rooms:")
            for room in rooms:
                print(f"{room.room_id}: {room.name}")
            try:
                room_id = int(input("Enter room ID: "))
                room = room_service.get_room_by_id(room_id)
                if not room:
                    raise ValueError()
            except ValueError:
                print("Invalid or unknown room ID.")
                continue

            date_str = input("Start date and time (YYYY-MM-DD HH:MM): ")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid date format.")
                continue

            try:
                duration = int(input("Duration in hours: "))
            except ValueError:
                print("Invalid duration.")
                continue

            try:
                booking = booking_service.create_booking(user, room, date, duration)
                print(f"Booking created: {booking}")
            except Exception as e:
                print(f"Error creating booking: {e}")

        elif choice == "6":
            bookings = booking_service.list_bookings()
            if not bookings:
                print("No bookings found.")
            for booking in bookings:
                print(booking)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    print("Welcome to the Meeting Room Booking System")
    main()