import editdistance


class Node(object):
    def __init__(self, index):
        self.index = index
        self.value = self.get_value(index)
        self.children = {}

    @staticmethod
    def get_value(index):
        return str(index)

    def __str__(self):
        return self.value


class Tree(object):
    def __init__(self, values=None, dis_func=None):
        self.root = None
        self.dis_func = dis_func
        if values:
            for value in values:
                self.add(value)

    def add(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            node = Node(value)
            top = self.root
            distance = self._distance(node, top)
            while distance in top.children.keys():
                top = top.children[distance]
                distance = self._distance(node, top)
            if distance == 0:
                print('distance is 0, so they are same')
            else:
                top.children[distance] = node
                node.parent = top

    def search(self, value, max_distance=2):
        candidates = [self.root]
        found = []

        while len(candidates) > 0:
            node = candidates.pop(0)
            distance = self._distance(node.value, value)

            if distance > max_distance:
                pass
            else:
                found.append(node.value)
            candidates.extend(node.children[dis] for dis in node.children.keys()
                              if abs(distance - max_distance) <= dis <= distance + max_distance)
        return found

    def _distance(self, a, b):
        a = a.value if isinstance(a, Node) else a
        b = b.value if isinstance(b, Node) else b
        if self.dis_func:
            return self.dis_func(a, b)
        else:
            return editdistance.eval(a, b)

    def __str__(self):
        candidates = [self.root]
        found = []
        while len(candidates) > 0:
            node = candidates.pop(0)
            found.append(node.value)
            candidates.extend(nd for nd in node.children.values())
        return str(found)

