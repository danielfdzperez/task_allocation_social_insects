import pygame
import random as rm
from server import *
from view import *
from random import shuffle
import numpy as np


def threshold_inc():
    return 10


RED = (255,0,0)
BLACK = (0,0,0)

pygame.init()

FPS = 20
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 30)

ctx = pygame.display.set_mode((1000,1000))

views = []
employees = []

n_tasks = 3
n_employees = 10

for i in range(n_employees):
    thresholds = np.random.randint(0,101,n_tasks)
    e = Server(thresholds, threshold_inc)
    employees.append( e )
    y = 105*(i%5)
    x = 150*(i//5)
    views.append( ServerView(e, (y,x)) )
employees = np.array(employees)

iteration = 0
while running:

    for e in employees:
        e.voteInitialization()

    indices = list(np.random.choice(n_employees, n_tasks, replace=False))
    voting = []

    for task in range(n_tasks):
        for employee in employees[indices]:
            voting.append(employee.voteTask())

        i = np.argmax(voting)
        employees[indices[i]].taskAssign(task)
        indices.pop(i)
        voting.clear()
    

    ctx.fill((0,0,0))
    for v in views:
        v.draw(ctx)

    #time_string = "Iteration {}".format(iteration)
    text = font.render("Press any key for new iteration", True, (255,255,255))
    ctx.blit(text, (150, 300))

    pygame.display.update()#flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                wait = False
            if event.type == pygame.KEYDOWN:
                wait = False

    iteration += 1

    #input("Press for new iteration")
    #clock.tick_busy_loop(FPS)

pygame.quit()
