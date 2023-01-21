from misc.queue.items.item import QueueItem


class PoleActionQueueItem(QueueItem):
    def __init__(self, pole_id:str, action:str):
        self.pole_id = pole_id
        self.action = action
        super().__init__("pole", (pole_id, action))

    def __str__(self):
        return f"{self.category} - {self.pole_id} - {self.action}"

    def __repr__(self):
        return str(self)