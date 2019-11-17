import pygame
from server import States as st

RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)



class View:


    def __init__(self, model ,position):
        self.position = position
        self.model = model
        self.font = pygame.font.SysFont("Times New Roman", 30)

    def draw(self,ctx):
        pass

class ServerView(View):
    COLORS = {st.BUSSY:RED, st.ON:GREEN, st.OFF:WHITE, st.DOWN:BLACK}
    def __init__(self, model ,position):
        super().__init__(model ,position)


    def draw(self, ctx):
        pygame.draw.rect(ctx, self.COLORS[self.model.state], pygame.Rect(self.position[0], self.position[1],100,100))
        string = "T {}".format(self.model.threshold)
        text = self.font.render(string, True, WHITE)
        ctx.blit(text, self.position)
        string = "Tasks {}".format(len(self.model.tasks))
        text = self.font.render(string, True, WHITE)
        ctx.blit(text, (self.position[0], self.position[1]+30))

class BrokerView(View):
    def __init__(self, model ,position):
        super().__init__(model ,position)

    def draw(self,ctx):
        pygame.draw.rect(ctx, BLUE, pygame.Rect(self.position[0], self.position[1],100,100))
        string = "Tasks {}".format(len(self.model.messages_tasks))
        text = self.font.render(string, True, WHITE)
        ctx.blit(text, self.position)


