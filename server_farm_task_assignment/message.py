class Message:
    def __init__(self, id_broker, id_task, forwarding):
        self.id_broker = id_broker #Id of the broker
        self.id_task = id_task #id Task
        self.forwarding = forwarding #True if this task is forwarding
