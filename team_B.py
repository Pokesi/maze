from queue_interface import Queue as QueueInterface


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue(QueueInterface):
    def __init__(self):
        self.front = None
        self.rear = None

    def put(self, value):
        new_node = Node(value)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def get(self):
        if self.empty():
            return None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return temp.value

    def empty(self):
        return self.front is None

    def size(self):
        count = 0
        current = self.front
        while current is not None:
            count += 1
            current = current.next
        return count
