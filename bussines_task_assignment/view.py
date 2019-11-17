import pygame

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
    COLORS = {False:RED, True:GREEN}
    def __init__(self, model ,position):
        super().__init__(model ,position)


    def draw(self, ctx):
        pygame.draw.rect(ctx, self.COLORS[self.model.selected], pygame.Rect(self.position[0], self.position[1],100,100))
        x = self.position[1]
        for i in range(len(self.model.task_threshold)):
            string = "T{} {}".format(i,self.model.task_threshold[i])
            text = self.font.render(string, True, WHITE)
            x = i
            ctx.blit(text, (self.position[0],self.position[1]+(i*30)))

        x = (x + 1) * 30
        string = "Task {}".format(self.model.assigend_task)
        text = self.font.render(string, True, WHITE)
        ctx.blit(text, (self.position[0], self.position[1]+x))
