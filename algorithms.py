import sys
import json
import os
import pickle

SAVE_PATH = 'fib_heap.pkl'

def load_heap():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, 'rb') as f:
            return pickle.load(f)
    return FibonacciHeap()

def save_heap(heap):
    with open(SAVE_PATH, 'wb') as f:
        pickle.dump(heap, f)

def clear_heap():
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)




class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

    def add_child(self, node):
        if not self.child:
            self.child = node
            node.left = node.right = node
        else:
            node.left = self.child
            node.right = self.child.right
            self.child.right.left = node
            self.child.right = node
        node.parent = self
        self.degree += 1

class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.n = 0
        self.nodes = []

    def insert(self, key):
        if self.find_node(key):
            print(f"[insert] Key {key} already exists. Insertion skipped.", file=sys.stderr)
            return  # Don't insert duplicate keys

        node = Node(key)
        self.nodes.append(node)
        if self.min is None:
            self.min = node
        else:
            node.left = self.min
            node.right = self.min.right
            self.min.right.left = node
            self.min.right = node
            if key < self.min.key:
                self.min = node
        self.n += 1

    def link(self, y, x):
        # Remove y from root list
        self.nodes.remove(y)

        # Make y a child of x
        y.parent = x
        y.left = y.right = y  # reset links
        if not x.child:
            x.child = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False

    def consolidate(self):
        A = [None] * 45  # Enough for ~2^45 nodes

        root_list = self.nodes[:]
        for w in root_list:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self.link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        # Rebuild the root list
        self.nodes = []
        self.min = None
        for node in A:
            if node:
                node.left = node.right = node
                self.nodes.append(node)
                if self.min is None or node.key < self.min.key:
                    self.min = node
    def to_visual_json(self):
        def walk(node):
            children = []
            if node.child:
                current = node.child
                while True:
                    children.append(walk(current))
                    current = current.right
                    if current == node.child:
                        break
            return {
                "name": str(node.key),
                "children": children,
            }

        roots = [walk(node) for node in self.nodes]
        return roots


    def delete_min(self):
        if not self.min:
            return

        z = self.min
        try:
            self.nodes.remove(z)
        except ValueError:
            pass

        # Promote min's children to root list
        if z.child:
            children = []
            current = z.child
            while True:
                children.append(current)
                current = current.right
                if current == z.child:
                    break
            for child in children:
                child.parent = None
                self.nodes.append(child)

        self.min = None
        if self.nodes:
            self.min = self.nodes[0]
            self.consolidate()

    def to_visual_json(self):
        def walk(node):
            children = []
            if node.child:
                current = node.child
                while True:
                    children.append(walk(current))
                    current = current.right
                    if current == node.child:
                        break
            return {"name": str(node.key), "children": children}

        roots = [walk(node) for node in self.nodes]
        return roots
    def find_node(self, key):
        def dfs(node):
            if node.key == key:
                return node
            if node.child:
                current = node.child
                while True:
                    result = dfs(current)
                    if result:
                        return result
                    current = current.right
                    if current == node.child:
                        break
            return None

        for node in self.nodes:
            result = dfs(node)
            if result:
                return result
        return None
    def cut(self, x, y):
        # Remove x from y's child list
        if y.child == x:
            if x.right != x:
                y.child = x.right
            else:
                y.child = None

        x.left.right = x.right
        x.right.left = x.left
        y.degree -= 1

        # Add x to root list
        x.parent = None
        x.left = x.right = x
        self.nodes.append(x)

    def cascading_cut(self, y):
        if y.parent:
            if not y.mark:
                y.mark = True
            else:
                z = y.parent
                self.cut(y, z)
                self.cascading_cut(z)
    def decrease_key(self, old_key, new_key):
        node = self.find_node(old_key)
        if not node:
            print(f"[decreaseKey] Node with key {old_key} not found", file=sys.stderr)
            return
        if new_key > node.key:
            print(f"[decreaseKey] New key {new_key} is not smaller than old key {old_key}", file=sys.stderr)
            return

        print(f"[decreaseKey] Updating key {old_key} to {new_key}", file=sys.stderr)
        node.key = new_key
        y = node.parent

        if y and node.key < y.key:
            self.cut(node, y)
            self.cascading_cut(y)

        if self.min is None or node.key < self.min.key:
            self.min = node


def main():
    heap = load_heap()
    try:
        data = json.loads(sys.stdin.readline())
        question = data.get("question", "")

        if question.startswith("insert"):
            _, val = question.split()
            heap.insert(int(val))
        elif question.strip() == "deleteMin":
            heap.delete_min()
        elif question.strip() == "clear":
            heap = FibonacciHeap()
            clear_heap()
        elif question.startswith("decreaseKey"):
            _, old_key, new_key = question.split()
            heap.decrease_key(int(old_key), int(new_key))


        save_heap(heap)
        output = heap.to_visual_json()
        print(json.dumps(output))

    except Exception as e:
        print(f"Error in Python script: {e}", file=sys.stderr)



if __name__ == "__main__":
    main()