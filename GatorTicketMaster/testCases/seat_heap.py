class SeatHeap:
    def __init__(self):
        self.seats = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def insert(self, seat_id):
        """Insert a new seat into the heap and maintain the min-heap property."""
        self.seats.append(seat_id)
        self._heapify_up(len(self.seats) - 1)

    def _heapify_up(self, index):
        """Ensure the heap property is maintained after insertion."""
        parent_index = self._parent(index)
        while index > 0 and self.seats[index] < self.seats[parent_index]:
            # Swap the current node with its parent
            self.seats[index], self.seats[parent_index] = self.seats[parent_index], self.seats[index]
            # Move up the heap
            index = parent_index
            parent_index = self._parent(index)

    def extract_min(self):
        """Remove and return the minimum seat (root of the heap)."""
        if self.is_empty():
            return None

        min_seat = self.seats[0]
        # Move the last element to the root and remove the last element
        self.seats[0] = self.seats[-1]
        self.seats.pop()
        # Heapify down to maintain the min-heap property
        if not self.is_empty():
            self._heapify_down(0)

        return min_seat

    def _heapify_down(self, index):
        """Ensure the heap property is maintained after removing the root."""
        left_index = self._left(index)
        right_index = self._right(index)
        smallest = index

        # Compare the current node with its left and right children
        if left_index < len(self.seats) and self.seats[left_index] < self.seats[smallest]:
            smallest = left_index
        if right_index < len(self.seats) and self.seats[right_index] < self.seats[smallest]:
            smallest = right_index

        # If the smallest node is not the current node, swap and continue heapifying down
        if smallest != index:
            self.seats[index], self.seats[smallest] = self.seats[smallest], self.seats[index]
            self._heapify_down(smallest)

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.seats) == 0

    def size(self):
        """Return the number of seats in the heap."""
        return len(self.seats)

    def peek(self):
        """Return the minimum seat without removing it."""
        if self.is_empty():
            return None
        return self.seats[0]

    def print_heap(self):
        """Print the heap for debugging purposes."""
        print(self.seats)
