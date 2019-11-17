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
        self.assigend_task = -1
        self.voting_threshole = None
        self.threshold_inc = threshold_inc #Function to increment the threshold

        self.selected = False

    def increaseThreshold(self, inc, i):
        self.task_threshold[i] = min((self.task_threshold[i] + inc),100)

    def voteInitialization(self):
        #Restart the parameters of the voting
        self.assigend_task = -1
        self.voting_threshole = list(self.task_threshold)
        self.selected = False

    def voteTask(self):
        vote = self.voting_threshole.pop(0)
        for v in self.voting_threshole:
            vote += (100-v)
        return vote

    def taskAssign(self,i):
        self.selected = True
        self.assigend_task = i #Assign the i task
        #Increase the threshold of the i task
        #because the skill in this task is better now
        self.increaseThreshold(self.threshold_inc(),i)
