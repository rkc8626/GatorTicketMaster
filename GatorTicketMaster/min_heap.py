class MinHeap:
    def __init__(self):
        self.heap = []
        self.position_map = {}  # Map userID to index for efficient updates

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def insert(self, priority, timestamp, userID):
        """Insert a new element into the heap as a tuple (priority, timestamp, userID)."""
        element = (priority, timestamp, userID)
        self.heap.append(element)
        self.position_map[userID] = len(self.heap) - 1
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """Heapify up to maintain the min-heap property based on (priority, timestamp)."""
        parent_index = self._parent(index)
        while index > 0 and self._compare(self.heap[index], self.heap[parent_index]) < 0:
            # Swap with parent
            self._swap(index, parent_index)
            # Move up the heap
            index = parent_index
            parent_index = self._parent(index)

    def extract_min(self):
        """Remove and return the smallest element from the heap."""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            self.position_map.pop(self.heap[0][2], None)
            return self.heap.pop()

        root = self.heap[0]
        # Move the last element to the root and heapify down
        self.heap[0] = self.heap.pop()
        self.position_map[self.heap[0][2]] = 0
        self.position_map.pop(root[2], None)
        self._heapify_down(0)
        return root

    def _heapify_down(self, index):
        """Heapify down to maintain the min-heap property based on (priority, timestamp)."""
        smallest = index
        left = self._left(index)
        right = self._right(index)

        if left < len(self.heap) and self._compare(self.heap[left], self.heap[smallest]) < 0:
            smallest = left
        if right < len(self.heap) and self._compare(self.heap[right], self.heap[smallest]) < 0:
            smallest = right

        # If the smallest is not the current index, swap and continue heapifying down
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _compare(self, a, b):
        """Comparison method for tuples (priority, timestamp, userID)."""
        # Compare by priority first, then timestamp
        if a[0] < b[0]:
            return -1
        elif a[0] > b[0]:
            return 1
        else:
            # If priorities are equal, compare by timestamp
            if a[1] < b[1]:
                return -1
            elif a[1] > b[1]:
                return 1
            return 0  # Equal priority and timestamp

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def size(self):
        """Return the current number of elements in the heap."""
        return len(self.heap)

    def _swap(self, i, j):
        """Swap elements at index i and j in the heap and update position_map."""
        self.position_map[self.heap[i][2]] = j
        self.position_map[self.heap[j][2]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def update_priority(self, userID, new_priority):
        """Update the priority of a user in the waitlist."""
        if userID not in self.position_map:
            print(f"User {userID} priority is not updated")
            return

        index = self.position_map[userID]
        current_priority, timestamp, _ = self.heap[index]
        # Update only if the new priority is different
        if new_priority != current_priority:
            self.heap[index] = (new_priority, timestamp, userID)
            # Decide to heapify up or down based on the new priority
            if new_priority < current_priority:
                self._heapify_up(index)
            else:
                self._heapify_down(index)
            print(f"User {userID} priority has been updated to {new_priority}")

    def remove_range(self, userID1, userID2):
        """Remove all entries with userID in the range [userID1, userID2]."""
        # Filter out entries within the range and keep others
        self.heap = [item for item in self.heap if not (userID1 <= item[2] <= userID2)]
        # Rebuild the position map and re-heapify
        self.position_map = {userID: i for i, (_, _, userID) in enumerate(self.heap)}
        # Heapify the entire structure
        for i in range(len(self.heap) // 2, -1, -1):
            self._heapify_down(i)
        print(f"Users in range [{userID1}, {userID2}] have been removed from the heap.")

