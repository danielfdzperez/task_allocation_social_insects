import random
from random import shuffle
import numpy as np

class Server:
    id = 0
    def __init__(self, task_threshold, threshold_inc):
        '''
            task_threshold -> List of thresholds for each task or numpy array
            threshold_inc -> function to increase the threshold
        '''
        self.id = Server.id
        Server.id += 1
        self.task_threshold = task_threshold #List with the threshold of each task
        self.assigned_task = -1
        self.threshold_inc = threshold_inc #Function to increment the threshold
        self.action_threshold = -1

    def increaseThreshold(self, inc, i):
        self.task_threshold[i] = min((self.task_threshold[i] + inc),100)

    def voteTask(self, i, repeated):
        vote = -1
        if self.assigned_task != -1:
            return vote

        if repeated:
            self.action_threshold += 10
        elif self.action_threshold > 0:
            self.action_threshold = -1

        u = random.random()*100
        if u <= self.task_threshold[i] or u <= self.action_threshold:
            vote = self.task_threshold[i]
        return vote

    def taskAssign(self,i):
        self.assigned_task = i #Assign the i task
        #Increase the threshold of the i task
        #because the skill in this task is better now
        self.increaseThreshold(self.threshold_inc(),i)
