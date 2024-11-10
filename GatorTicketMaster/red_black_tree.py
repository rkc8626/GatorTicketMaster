class RedBlackTree:
    class Node:
        def __init__(self, key, value, color="RED", parent=None, left=None, right=None):
            self.key = key  # user_id
            self.value = value  # seat_id
            self.color = color
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        self.NIL_LEAF = self.Node(key=None, value=None, color="BLACK")  # Sentinel node (for leaves)
        self.root = self.NIL_LEAF

    def is_empty(self):
        """Check if the Red-Black Tree is empty."""
        return self.root == self.NIL_LEAF

    def max_seat(self):
        """Find the maximum seat ID in the tree."""
        current = self.root
        if self.is_empty():
            return None
        while current.right != self.NIL_LEAF:
            current = current.right
        return current.value  # This is the maximum seat_id

    def search(self, key):
        """Search for a node with the given key (user_id) and return its value (seat_id)."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node == self.NIL_LEAF or node.key is None:
            return None  # Not found
        if key == node.key:
            return node.value  # Return seat_id
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def insert(self, key, value):
        """Insert a new node with the given key (user_id) and value (seat_id)."""
        new_node = self.Node(key=key, value=value, left=self.NIL_LEAF, right=self.NIL_LEAF)
        parent = None
        current = self.root

        # Binary Search Tree insert logic
        while current != self.NIL_LEAF:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            # Tree is empty
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = "RED"
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        """Fix the Red-Black Tree after an insertion to maintain the properties."""
        while node != self.root and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == "RED":
                    # Case 1: Uncle is red
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    # Case 2 and 3: Uncle is black
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == "RED":
                    # Case 1: Uncle is red
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    # Case 2 and 3: Uncle is black
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_left(node.parent.parent)
        self.root.color = "BLACK"

    def _rotate_left(self, node):
        """Rotate the node to the left."""
        y = node.right
        node.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def _rotate_right(self, node):
        """Rotate the node to the right."""
        y = node.left
        node.left = y.right
        if y.right != self.NIL_LEAF:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def delete(self, key):
        """Delete the node with the given key (user_id) from the Red-Black Tree."""
        node = self._search_node(self.root, key)
        if node == self.NIL_LEAF or node.key is None:
            return  # Node to be deleted does not exist

        y_original_color = node.color
        if node.left == self.NIL_LEAF:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL_LEAF:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _fix_delete(self, x):
        """Fix the Red-Black Tree after a deletion to maintain the properties."""
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self._rotate_left(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    sibling.color = "RED"
                    x = x.parent
                else:
                    if sibling.right.color == "BLACK":
                        sibling.left.color = "BLACK"
                        sibling.color = "RED"
                        self._rotate_right(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.right.color = "BLACK"
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self._rotate_right(x.parent)
                    sibling = x.parent.left
                if sibling.right.color == "BLACK" and sibling.left.color == "BLACK":
                    sibling.color = "RED"
                    x = x.parent
                else:
                    if sibling.left.color == "BLACK":
                        sibling.right.color = "BLACK"
                        sibling.color = "RED"
                        self._rotate_left(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.left.color = "BLACK"
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = "BLACK"

    def _minimum(self, node):
        """Find the minimum value node starting from the given node."""
        while node.left != self.NIL_LEAF:
            node = node.left
        return node

    def _transplant(self, u, v):
        """Replace the subtree rooted at node u with the subtree rooted at node v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _search_node(self, node, key):
        """Search for a node by its key (user_id)."""
        if node == self.NIL_LEAF or key == node.key:
            return node
        if key < node.key:
            return self._search_node(node.left, key)
        else:
            return self._search_node(node.right, key)

    def inorder(self):
        """Inorder traversal of the Red-Black Tree and returns the reservations as a list of tuples."""
        result = []

        def _inorder_helper(node):
            if node != self.NIL_LEAF:
                _inorder_helper(node.left)
                result.append((node.value, node.key))  # Append (seat_id, user_id)
                _inorder_helper(node.right)

        _inorder_helper(self.root)
        return result  # Return the list of (seat_id, user_id) tuples


    def contains(self, user_id):
        """Check if the tree contains the given user_id."""
        result = self._search_node(self.root, user_id)
        return result != self.NIL_LEAF

    def in_order_traversal(self):
        """Perform an in-order traversal and return a list of (seatID, userID) pairs."""
        results = []
        self._in_order_helper(self.root, results)
        return results

    def _in_order_helper(self, node, results):
        """Recursive helper for in-order traversal."""
        if node != self.NIL_LEAF:
            self._in_order_helper(node.left, results)
            results.append((node.value, node.key))  # Collect (seatID, userID) pairs
            self._in_order_helper(node.right, results)
