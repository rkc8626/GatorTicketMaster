## Gator Ticket Master Project Report

### Project Overview

Gator Ticket Master is a software system designed to manage seat reservations and allocations for events. It supports various operations, including reserving seats, canceling reservations, updating waitlist priorities, and releasing seats. The project is built with efficiency in mind, using a Red-Black Tree for reservation management and a MinHeap for managing a priority-based waitlist. This report outlines the structure of the project, including the function prototypes, design choices, and an overview of the data flow and logic used to implement the system.

---

### Project Structure

The project is organized into four main files:

1. **`gatorTicketMaster.py`**: The main module responsible for processing user commands related to seat management and executing operations such as reserving seats, canceling reservations, updating priorities, and managing the waitlist.
  
2. **`min_heap.py`**: Implements a MinHeap data structure to handle the priority-based waitlist. The MinHeap efficiently manages users waiting for a reservation by allowing quick access to the user with the highest priority.

3. **`red_black_tree.py`**: Implements a Red-Black Tree to manage seat reservations. The Red-Black Tree enables efficient insertion, deletion, and retrieval of reservations while maintaining sorted order by user ID, allowing for quick access and efficient management of reserved seats.

4. **`Makefile`**: Contains build and run commands to streamline the process of executing the main program. This allows users to quickly launch the program by running a single command with a specified input file.

---

### Makefile Commands

The **Makefile** automates the execution of the `gatorTicketMaster.py` script and simplifies project operations. It includes the following command:

```makefile
gatorTicketMaster:
	python3 gatorTicketMaster.py $(file_name)
```

- **Command `gatorTicketMaster`**: Executes the main script `gatorTicketMaster.py`, where `file_name` is an input file containing commands that are processed by the system to perform various operations. This command makes it easy to run the program by specifying only the name of the input file, allowing users to test different configurations or inputs without modifying the code.

---

### Core Function Prototypes and Brief Descriptions

#### gatorTicketMaster.py

- **`process_input(file_name: str)`**: Reads commands from an input file and directs each command to the corresponding function, managing various seat operations (e.g., reserve, cancel, add seats).

- **`add_seats(count: int)`**: Adds a specified number of seats to the available pool, increasing the total seats for reservation.

- **`reserve(user_id: int, user_priority: int)`**: Attempts to reserve a seat for a user. If no seats are available, the user is added to a waitlist, prioritized by `user_priority`.

- **`cancel(seat_id: int, user_id: int)`**: Cancels an existing reservation for a specific user and seat. If users are on the waitlist, it allocates the seat to the highest-priority user in the waitlist.

- **`update_priority(user_id: int, new_priority: int)`**: Updates a user’s priority in the waitlist. This function reorders the MinHeap to reflect the updated priority.

- **`release_seats(user_id1: int, user_id2: int)`**: Releases seats by removing a range of users (from `user_id1` to `user_id2`) from the waitlist, useful for clearing out users who are no longer interested.

- **`exit_waitlist(user_id: int)`**: Removes a specific user from the waitlist without affecting other users.

- **`print_reservations()`**: Lists all current reservations in the system in order of user ID by performing an in-order traversal of the Red-Black Tree.

- **`save_output()`**: Ensures the system’s output is saved even if the `Quit` command is not explicitly called, preserving all session data.

---

#### min_heap.py

- **`__init__()`**: Initializes the MinHeap data structure with an empty list and a mapping (`position_map`) to track the positions of elements for efficient access.

- **`insert(priority: int, timestamp: int, element: Any)`**: Inserts an element into the heap with a specified priority and timestamp (for tie-breaking). It positions the element based on the MinHeap property.

- **`_heapify_up(index: int)`**: Moves an element up in the heap to maintain the MinHeap structure. Used after an insertion or update operation.

- **`delete(element: Any)`**: Removes a specified element from the heap. If not the last element, it replaces the element with the last one and reorders the heap.

- **`extract_min()`**: Retrieves and removes the element with the lowest priority from the heap, essential for managing the waitlist by priority.

- **`update_priority(element: Any, new_priority: int)`**: Updates the priority of a specific element, reorganizing the heap to reflect the new priority.

- **`remove_range(start: Any, end: Any)`**: Removes all elements within a specified range from the heap, efficiently clearing out multiple users if needed.

---

#### red_black_tree.py

- **`Node.__init__(key, value, color="RED", parent=None, left=None, right=None)`**: Defines a Red-Black Tree node with a user ID (`key`), seat ID (`value`), color (defaulting to RED), and pointers for tree structure.

- **`insert(key: Any, value: Any)`**: Inserts a new node into the tree with a user ID as the key and seat ID as the value. After insertion, the tree balances itself to maintain Red-Black Tree properties.

- **`_fix_insert(node: Node)`**: Adjusts the tree to ensure Red-Black properties after an insertion. Balances the tree by changing colors or rotating nodes as needed.

- **`delete(key: Any)`**: Removes a node with a given user ID from the tree, performing rebalancing operations as needed to maintain tree properties.

- **`_fix_delete(x: Node)`**: Restores Red-Black properties after a node deletion by rebalancing the tree as necessary.

- **`inorder()`**: Returns an in-order traversal of the tree, listing all reservations by seat and user IDs.

---

### Programming Choices and Rationale

The system employs two main data structures: a **MinHeap** for the waitlist and a **Red-Black Tree** for reservation management.

#### MinHeap for Waitlist Management
- The **MinHeap** allows efficient insertion and retrieval of users based on priority, supporting a priority queue where the user with the lowest priority number is served first.
- This structure ensures fast access to the highest-priority user and minimizes the time complexity for insertion and deletion operations.
- **Pros**: Efficient for priority-based retrieval; suitable for managing a dynamic queue of users.
- **Cons**: Does not inherently maintain sorted order, as it is optimized for accessing the minimum element.

#### Red-Black Tree for Reservation Management
- The **Red-Black Tree** is used to track reserved seats by user ID. Its self-balancing property ensures efficient insertions, deletions, and in-order traversal, ideal for maintaining a sorted list of reservations.
- **Pros**: Provides quick access, maintains sorted order, and guarantees balanced structure.
- **Cons**: More complex to implement and maintain than simpler data structures, though the added complexity ensures efficiency.

---

### Logic and Data Flow

1. **Adding Seats**: The system can increase available seats through `add_seats()`, which increases the total seat count. This function is essential for expanding the pool of seats during high-demand periods.

2. **Reserving Seats**: The `reserve()` function checks if seats are available and, if so, assigns a seat to the user. If no seats are available, the user is added to the waitlist based on their priority. If seats become available later, the highest-priority user in the waitlist is automatically assigned a seat.

3. **Canceling Reservations**: `cancel()` removes a user’s reservation, freeing the seat for another user. The function immediately checks the waitlist to assign the available seat to the highest-priority user.

4. **Updating Priority**: When a user’s priority changes, the `update_priority()` function adjusts their position in the waitlist based on the new priority. This function ensures that users are always organized correctly according to priority.

5. **Releasing Seats**: The `release_seats()` function clears a range of users from the waitlist, allowing the system to remove users who may no longer be interested in waiting.

6. **Displaying Reservations**: Using an in-order traversal of the Red-Black Tree, `print_reservations()` lists all active reservations in sorted order. This traversal method ensures that the reservations are output in a logical and easily readable format.

---

### Summary

The Gator Ticket Master system is designed with efficiency and scalability in mind, leveraging advanced data structures to manage seats and reservations. The project’s modular architecture, combined with the use of Red-Black Trees and MinHeaps, ensures that operations are performed quickly, even under high demand. This report provides an in-depth look at the structure, functionality, and logic underpinning the system, outlining the design choices and considerations that enable Gator Ticket Master to manage reservations effectively.
