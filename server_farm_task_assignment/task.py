class Task:
    current_id = 0
    def __init__(self, time, type):
        self.id = Task.current_id #id of the task
        Task.current_id += 1
        self.time = time #time to do the task
        self.type = type #Type of the task
        self.current_time = 0 #Current time doing the task

    def do(self):
        self.current_time += 1
        return self.current_time >= self.time
