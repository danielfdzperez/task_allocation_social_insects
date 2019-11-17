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
n_employees = 30

for i in range(n_employees):
    thresholds = np.random.randint(0,101,n_tasks)
    e = Server(thresholds, threshold_inc)
    employees.append( e )
    y = 105*(i%8)
    x = 151*(i//8)
    views.append( ServerView(e, (y,x)) )
employees = np.array(employees)

iteration = 0
assigned_tasks = 0
while running:

    voting = []

    task = random.randint(0,n_tasks-1)
    not_asigned = True
    repeat = False
    while not_asigned: 

        for employee in employees:
            voting.append(employee.voteTask(task, repeat))

        if np.max(voting) != -1:
            i = np.argmax(voting)
            employees[i].taskAssign(task)
            not_asigned = False
            assigned_tasks += 1

        repeat = True

        voting.clear()

    ctx.fill((0,0,0))
    for v in views:
        v.draw(ctx)

    string = "Press any key for new iteration   Allocated task {}".format(task)
    text = font.render(string, True, (255,255,255))
    ctx.blit(text, (150, 600))

    pygame.display.update()#flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                wait = False

            if event.type == pygame.KEYDOWN:
                wait = False
                if assigned_tasks >= n_employees:
                    running = False

    iteration += 1

    #input("Press for new iteration")
    #clock.tick_busy_loop(FPS)

pygame.quit()
