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
