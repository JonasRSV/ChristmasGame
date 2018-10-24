class Node(object):
    def __init__(self, parent: Node = None, depth: int = 0):
        self.parent = parent
        self.depth = depth

        self.left_child = None
        self.right_child = None


class PriorityQueue(object):
    def __init__(self,
                 root=None,
                 comparator=lambda x, y: (x, y) if x > y else (y, x)):

        self.root = root
        self.comparator = comparator

    def __add_from(self, node: Node, item: "generic") -> None:
        pass

    def add(self, item: "generic") -> None:
        if self.root is None:
            self.root = item
        else:
            self.__add_from(self.root, item)
