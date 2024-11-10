from red_black_tree import RedBlackTree
from min_heap import MinHeap

# Additional Testing for MinHeap
def extended_test_min_heap():
    print("Extended Testing for MinHeap...\n")

    # Initialize the MinHeap
    heap = MinHeap()

    # Insert elements with different priorities and timestamps
    heap.insert(1, 1, 100)  # (priority, timestamp, userID)
    heap.insert(2, 2, 200)
    heap.insert(1, 3, 300)
    heap.insert(1, 4, 400)
    print("Heap after insertions with mixed priority and timestamps:", heap.heap)

    # Extract minimum element to check priority and timestamp ordering
    min_element = heap.extract_min()
    print("Extracted min element (expecting userID=100):", min_element)
    print("Heap after extracting min:", heap.heap)

    # Insert another element and extract again
    heap.insert(1, 5, 500)  # Higher priority with latest timestamp
    min_element = heap.extract_min()
    print("Extracted min element (expecting userID=300):", min_element)
    print("Heap after extracting min:", heap.heap)

    # Test remove_range functionality with multiple matches
    heap.insert(3, 6, 600)
    heap.insert(2, 7, 700)
    heap.insert(2, 8, 800)
    print("Heap before removing range [200, 700]:", heap.heap)
    heap.remove_range(200, 700)
    print("Heap after removing range [200, 700]:", heap.heap)

# Additional Testing for RedBlackTree
def extended_test_red_black_tree():
    print("\nExtended Testing for RedBlackTree...\n")

    # Initialize the RedBlackTree
    tree = RedBlackTree()

    # Insert nodes (userID, seatID) in an order to verify correct balancing
    tree.insert(100, 1)
    tree.insert(200, 2)
    tree.insert(300, 3)
    tree.insert(150, 4)
    tree.insert(250, 5)
    print("Tree after multiple insertions (in-order traversal):", tree.in_order_traversal())

    # Search for a node by userID
    seat_id = tree.search(200)
    print("Seat ID for userID=200 (expecting 2):", seat_id)

    # Delete nodes and verify structure
    tree.delete(200)
    tree.delete(300)
    print("Tree after deleting userID=200 and userID=300 (in-order traversal):", tree.in_order_traversal())

    # Insert additional nodes after deletion to verify balance
    tree.insert(275, 6)
    print("Tree after inserting userID=275 (in-order traversal):", tree.in_order_traversal())

# Run the extended tests
extended_test_min_heap()
extended_test_red_black_tree()
