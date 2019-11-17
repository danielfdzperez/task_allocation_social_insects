from enum import Enum 
from message import *
from task import *
import random
from random import shuffle

#From https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
def enum(**enums):
    return type('Enum', (), enums)
States = enum(BUSSY=0, ON=1, OFF=2, DOWN=3)

class Server:
    id = 0
    def __init__(self, threshold_inc, threshold_dec,max_tasks, brokers, p_error = 0, error_iterations= 50, threshold = 0, time_decrase_threshold = 2,on=False):
        self.id = Server.id
        Server.id += 1
        self.threshold = threshold #Current threshold
        self.threshold_dec = threshold_dec
        self.threshold_inc = threshold_inc #Function to increment the threshold
        self.max_tasks = max_tasks #Maximum number of tasks
        self.messages = [] #List of pending messages
        self.time_decrase_threshold = time_decrase_threshold
        self.c_t_decrease_threshold = 0
        #For simulation, in real application is not needed
        self.on = on #True if server is on
        self.tasks = []
        self.brokers = brokers #List of the brokers SIMULATION
        self.p_error = p_error #Probability that a server has an error
        self.error_iterations = error_iterations #Number of iterations broken
        self.current_error_iterations = 0 #Current number of iterations broken
        if self.on:
            self.state = States.ON
        else:
            self.state = States.OFF

        self.executeIteration = self.iteration

    def iteration(self):
        self.c_t_decrease_threshold += 1
        #self.requestTask()
        done = []
        #Execute one step for each task
        for task in self.tasks:
            if task.do():
                done.append(task)
        #For each task that is ended, remove from the list
        for task in done:
           self.tasks.remove(task)

        if len(self.tasks) > 0:
            self.increasethreshold(self.threshold_inc(self.threshold, False, len(self.tasks)))

        #Each x times decrease the threshold if no task in execution
        #if len(self.tasks) is 0 and self.c_t_decrease_threshold >= self.time_decrase_threshold:
        if self.c_t_decrease_threshold >= self.time_decrase_threshold:
            self.decreasethreshold(self.threshold_dec(self.threshold, len(self.tasks), self.max_tasks))
            self.c_t_decrease_threshold = 0


        #For simulation
        if len(self.tasks) is self.max_tasks:
            if self.state is not States.BUSSY:
                self.state = States.BUSSY
        elif len(self.tasks) > 0 and self.state is not States.ON:
            self.state = States.ON

        self.maybeBroken()

        #Falta decrementar threshold si no ejecutamos nada ¿o pocas tareas?


    def broken(self):
        #If the server is broken, add broken iteration
        self.current_error_iterations += 1
        #If is repaired then change the state and reset all the stats
        if self.current_error_iterations >= self.error_iterations:
            self.state = States.ON
            self.current_error_iterations = 0
            self.executeIteration = self.iteration
            self.c_t_decrease_threshold = 0

    def maybeBroken(self):
        u = random.random()
        #Test if the server is broken
        if u <= self.p_error:
            self.state = States.DOWN
            self.threshold = 0
            self.tasks.clear()
            self.executeIteration = self.broken

    def increasethreshold(self, inc):
        self.threshold = min((self.threshold + inc),100)

    def decreasethreshold(self, dec):
        self.threshold = max((self.threshold - dec),0)

    def requestTask(self):
        #Get all the possible tasks from the brokers
        #Not efficient but works for this simulation
        u = random.random()
        #shuffle(self.messages) #For simulation
        #Possible to get more than one message from each server
        for message in self.messages:
            #Se puede jugar cuando se incremetna el threshold
            #If there is space for more task and the random value is in the threshold
            #print(str(self.id),str(u*100),str(self.threshold))
            if len(self.tasks) < self.max_tasks and self.threshold >= u*100:
                #Get the task
                task = self.brokers[message.id_broker].sendTask(message.id_task)
                #If any server got the task, add the task and increase the threshold
                if task.type is not 0:
                    self.tasks.append(task)
                    #self.increasethreshold(self.threshold_inc(self.threshold, False))
            elif message.forwarding:
                #If i dont get the task and the task is forwarding, increase the threshold
                self.increasethreshold(self.threshold_inc(self.threshold, True))
            #elif len(self.tasks) > 0:
            #    self.increasethreshold(self.threshold_inc(self.threshold, False))
        #Clear message list
        self.messages.clear()

    
    def receiveMessage(self,message):
        if self.state is not States.DOWN:
            self.messages.append(message)
            #self.messages += messages
        self.requestTask()
