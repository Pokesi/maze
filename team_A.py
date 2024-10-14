from queue_interface import Queue as QueueInterface


class Queue(QueueInterface):
    def __init__(self):
        self.queue = []

    def put(self, value):
        self.queue.append(value)

    def get(self):
        if not self.empty():
            return self.queue.pop(0)

    def empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
