from red_black_tree import RedBlackTree
from min_heap import MinHeap
import sys
import os

class GatorTicketMaster:
    def __init__(self, output_file):
        self.available_seats = MinHeap()
        self.reserved_seats = RedBlackTree()
        self.waitlist = MinHeap()
        self.output_file = output_file
        self.output_lines = []
        self.timestamp = 0  # Used for ordering users on the waitlist
        self.total_seats = 0  # Tracks the total seats initialized or added


    def _write_output(self, message):
        self.output_lines.append(message)
        print(f"[DEBUG] {message}")  # Debug statement to trace operations

    def save_output(self):
        with open(self.output_file, 'w') as f:
            f.write("\n".join(self.output_lines))

    def initialize(self, seat_count):
        """Initialize available seats and set total seats."""
        for seat in range(1, seat_count + 1):
            self.available_seats.insert(seat, 0, 0)  # Using seat number as priority for MinHeap
        self.total_seats = seat_count
        self._write_output(f"{seat_count} Seats are made available for reservation")

    def available(self):
        """Show the number of available seats and waitlist size."""
        available_count = self.available_seats.size()
        waitlist_length = len(self.waitlist.heap)
        self._write_output(f"Total Seats Available : {available_count}, Waitlist : {waitlist_length}")



    def reserve(self, userID, userPriority):
        """Reserve a seat for the user if available, else add to waitlist."""
        if not self.available_seats.is_empty():
            seat = self.available_seats.extract_min()[0]
            self.reserved_seats.insert(userID, seat)
            self._write_output(f"User {userID} reserved seat {seat}")
        else:
            self.waitlist.insert(userPriority, self.timestamp, userID)
            self.timestamp += 1
            self._write_output(f"User {userID} is added to the waiting list")

    def cancel(self, seatID, userID):
        """Cancel a reservation. Reassign seat if there's a waitlist, else add to available."""
        current_seat = self.reserved_seats.search(userID)
        if current_seat == seatID:
            self.reserved_seats.delete(userID)
            if not self.waitlist.is_empty():
                priority, timestamp, waitlist_user = self.waitlist.extract_min()
                self.reserved_seats.insert(waitlist_user, seatID)
                self._write_output(f"User {userID} canceled their reservation\nUser {waitlist_user} reserved seat {seatID}")
            else:
                # If no waitlist users, add seat back to available
                self.available_seats.insert(seatID, 0, 0)
                self._write_output(f"User {userID} canceled their reservation")
        else:
            # Handle invalid cancellation attempt
            self._write_output(f"User {userID} has no reservation for seat {seatID} to cancel")

    def add_seats(self, count):
        """Add new seats, assigning them to waitlist users first if any."""
        start_seat = self.total_seats + 1
        self.total_seats += count
        self._write_output(f"Additional {count} Seats are made available for reservation")

        for seat_id in range(start_seat, start_seat + count):
            if not self.waitlist.is_empty():
                priority, timestamp, waitlist_user = self.waitlist.extract_min()
                self.reserved_seats.insert(waitlist_user, seat_id)
                self._write_output(f"User {waitlist_user} reserved seat {seat_id}")
            else:
                # Add new seats to available seats if no one is on the waitlist
                self.available_seats.insert(seat_id, 0, 0)

    def update_priority(self, userID, new_priority):
        # Check if the user is in the waitlist
        found = False
        for i, (priority, timestamp, uid) in enumerate(self.waitlist.heap):
            if uid == userID:
                # Update the user with the new priority, keeping the original timestamp
                found = True
                _, original_timestamp, _ = self.waitlist.heap.pop(i)
                self.waitlist._rebuild_heap()  # Restore heap property after removal
                self.waitlist.insert(new_priority, original_timestamp, userID)
                self._write_output(f"User {userID} priority has been updated to {new_priority}")
                break

        if not found:
            # If the user is not in the waitlist
            self._write_output(f"User {userID} priority is not updated")

    def exit_waitlist(self, userID):
        # Locate the user in the waitlist
        found = False
        for i, (priority, timestamp, uid) in enumerate(self.waitlist.heap):
            if uid == userID:
                # Remove the user and rebuild the heap
                found = True
                self.waitlist.heap.pop(i)
                self.waitlist._rebuild_heap()  # Restore heap after removal
                self._write_output(f"User {userID} is removed from the waiting list")
                break

        if not found:
            # User was not in the waitlist
            self._write_output(f"User {userID} is not in waitlist")


    def release_seats(self, userID1, userID2):
        """Release all seats held by users within the range [userID1, userID2]."""
        released_seats = []
        for user_id in range(userID1, userID2 + 1):
            seat_id = self.reserved_seats.search(user_id)
            if seat_id:
                self.reserved_seats.delete(user_id)
                released_seats.append(seat_id)

        released_seats.sort()
        self.waitlist.remove_range(userID1, userID2)

        self._write_output(f"Reservations of the Users in the range [{userID1}, {userID2}] are released")

        for seat_id in released_seats:
            if not self.waitlist.is_empty():
                priority, timestamp, next_user = self.waitlist.extract_min()
                self.reserved_seats.insert(next_user, seat_id)
                self._write_output(f"User {next_user} reserved seat {seat_id}")
            else:
                # If no users in waitlist, seat goes back to available seats
                self.available_seats.insert(seat_id, 0, 0)


    def print_reservations(self):
        reservations = self.reserved_seats.in_order_traversal()
        for seat, user in sorted(reservations, key=lambda x: x[0]):
            self._write_output(f"Seat {seat}, User {user}")


    def quit(self):
        self._write_output("Program Terminated!!")
        self.save_output()
        sys.exit(0)

def process_input(input_file):
    # Create the output file name by appending "_output_file.txt" to the input file name (without extension)
    input_filename_without_ext = os.path.splitext(input_file)[0]
    output_file = f"{input_filename_without_ext}_output_file.txt"

    # Initialize the system with the output file name
    system = GatorTicketMaster(output_file)

    with open(input_file, 'r') as file:
        for line in file:
            # Split command and arguments
            command = line.strip().split('(')
            operation = command[0].strip()

            # Handle Initialize(seatCount)
            if operation == "Initialize":
                seat_count = int(command[1][:-1])  # Extract seat count
                system.initialize(seat_count)

            # Handle Available()
            elif operation == "Available":
                system.available()

            # Handle Reserve(userID, userPriority)
            elif operation == "Reserve":
                params = command[1][:-1].split(',')
                user_id = int(params[0].strip())
                user_priority = int(params[1].strip())
                system.reserve(user_id, user_priority)

            # Handle Cancel(seatID, userID)
            elif operation == "Cancel":
                params = command[1][:-1].split(',')
                seat_id = int(params[0].strip())
                user_id = int(params[1].strip())
                system.cancel(seat_id, user_id)

            # Handle AddSeats(count)
            elif operation == "AddSeats":
                try:
                    count = int(command[1][:-1].strip())  # Extract seat count to add
                    system.add_seats(count)
                except ValueError:
                    system._write_output("Invalid input. Please provide a valid number of seats.")

            # Handle ReleaseSeats(userID1, userID2)
            elif operation == "ReleaseSeats":
                params = command[1][:-1].split(',')
                user_id1 = int(params[0].strip())
                user_id2 = int(params[1].strip())
                system.release_seats(user_id1, user_id2)

            # Handle UpdatePriority(userID, userPriority)
            elif operation == "UpdatePriority":
                params = command[1][:-1].split(',')
                user_id = int(params[0].strip())
                new_priority = int(params[1].strip())
                system.update_priority(user_id, new_priority)

            # Handle ExitWaitlist(userID)
            elif operation == "ExitWaitlist":
                user_id = int(command[1][:-1].strip())
                system.exit_waitlist(user_id)

            # Handle PrintReservations()
            elif operation == "PrintReservations":
                system.print_reservations()

            # Handle Quit()
            elif operation == "Quit":
                system.quit()

    # Ensure that output is saved even if the 'Quit()' command is not explicitly called
    system.save_output()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gatorTicketMaster.py <input_file>")
        sys.exit(1)
    process_input(sys.argv[1])
