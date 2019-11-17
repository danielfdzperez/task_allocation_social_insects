from task import *
from message import *
from random import shuffle
import random

class Broker:
    id = 0
    def __init__(self, makeTask, max_iterations, max_task_time):
        self.servers = []#servers #List of servers
        self.id = Broker.id
        Broker.id += 1
        self.makeTask = makeTask
        self.tasks = []
        self.max_iterations = max_iterations
        self.iteration = 0
        self.task0 = Task(0,0)
        self.messages_tasks = []
        self.max_task_time = max_task_time

    def addServers(self,servers):
        self.servers = servers
    def executeIteration(self):

        #for m in self.messages_tasks:
        #    m[1].forwarding = True

        if self.makeTask(self.iteration):
            self.createTask()

        self.iteration = (self.iteration + 1) % self.max_iterations 
        self.sendMessages()

    def createTask(self):
        time = random.randint(1,self.max_task_time)
        #type = random.randint(1,self.max_task_time)
        task = Task(time, 1)
        message = Message(self.id, task.id, 0)  
        self.messages_tasks.append((task,message))

    def sendMessages(self):
        if not self.messages_tasks:
            return

        #messages = [m_t[1] for m_t in self.messages_tasks]
        #for server in self.servers:
        #    server.receiveMessage(messages)
        message = self.messages_tasks[0][1]
        
        shuffle(self.servers)#Simulation, emulate round robin (paralelism)
        for server in self.servers:
            server.receiveMessage(message)

        if not message.forwarding:
            message.forwarding = True


    def sendTask(self, task_id):
        task = self.task0
        for index, tup in enumerate(self.messages_tasks):
            if tup[0].id == task_id:
                task = self.messages_tasks.pop(index)[0]
                break
        return task


