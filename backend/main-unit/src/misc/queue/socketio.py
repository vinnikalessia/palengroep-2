from misc.queue import QueueItem


class SocketQueueItem(QueueItem):
    def __init__(self, message):
        super().__init__("socketio", message)
