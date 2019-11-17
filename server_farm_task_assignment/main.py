import pygame
import random as rm
from broker import *
from server import *
from view import *
from random import shuffle

def makeTask(iteration):
    return rm.random() <= 0.2

def threshold_inc(threshold, forwarding, t=0, mt=0):
    if not forwarding:
        if t <= 3:
            return 1
        return 5
    return 10

def threshold_dec(threshold, t, mt):

    if t is 0:
        return 5
    return 0#(mt - t)*10


RED = (255,0,0)
BLACK = (0,0,0)

pygame.init()

FPS = 20
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 30)

ctx = pygame.display.set_mode((1000,1000))

brokers = []
views = []
servers = []

n_brokers = 1
n_servers = 3

for i in range(n_brokers):
    broker = Broker(makeTask, 5, 20)
    brokers.append(broker)
    views.append(BrokerView(broker, (i*150+50,50)))

for i in range(n_servers):
    server = Server(threshold_inc, threshold_dec, 5,brokers, p_error=0.01, on=True)
    servers.append(server)
    views.append(ServerView(server, (i*150+50,300)))

for b in brokers:
    b.addServers(servers)


iteration = 0
while running:

    #pygame.draw.rect(ctx, RED, pygame.Rect(10, 10, 100, 100))
    #time_string = ""#"{}".format(pygame.time.get_ticks()/1000)
    #text = font.render(time_string, True, BLACK)
    #ctx.blit(text, (10, 10))

    for b in brokers:
        b.executeIteration()

    shuffle(servers)
    for s in servers:
        s.executeIteration()

    ctx.fill((0,0,0))
    for v in views:
        v.draw(ctx)
    time_string = "Iteration {}".format(iteration)
    text = font.render(time_string, True, (255,255,255))
    ctx.blit(text, (150*(n_brokers+1), 10))

    brokers_string = "Brokers"
    text = font.render(brokers_string, True, (255,255,255))
    ctx.blit(text, (150*(n_brokers), 50))

    servers_string = "Servers"
    text = font.render(servers_string, True, (255,255,255))
    ctx.blit(text, (150*(n_servers), 300))

    pygame.display.update()#flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    iteration += 1

    #input()
    clock.tick_busy_loop(FPS)

pygame.quit()
