from queue import Queue
from typing import Dict, Type


class QueueItem:
    def __init__(self, category: str, payload: any):
        self.category = category
        self.payload = payload

    def __str__(self):
        return f"{self.category} - {self.payload}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, QueueItem):
            return self.category == other.category and self.payload == other.payload
        return False

    def __hash__(self):
        return hash((self.category, self.payload))


class MQTTQueueItem(QueueItem):
    def __init__(self, topic: str, payload: any):
        self.topic = topic
        super().__init__("mqtt", {"topic": topic, "payload": payload})

    def __str__(self):
        return f"{self.category} - {self.topic} - {self.payload}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, MQTTQueueItem):
            return self.topic == other.topic and self.payload == other.payload
        return False

    def __hash__(self):
        return hash((self.category, self.topic, self.payload))


GameMessageQueue = Queue[QueueItem]
