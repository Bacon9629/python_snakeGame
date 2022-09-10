import random
import pygame
from parameter import Parameter


pygame.init()

class Goal(Parameter):
    def __init__(self):
        super().__init__()
        self.goal_width = 20

    def get_goal(self,snake_list) -> object:
        goal = self.__generate_goal()
        while goal in snake_list:
           goal = self.__generate_goal()
        
        return goal

    def __generate_goal(self) -> object:
        x = random.randrange(0, self.win_width - self.goal_width, self.goal_width)
        y = random.randrange(0, self.win_height - self.goal_width, self.goal_width)
        goal = pygame.Rect(x, y, 20, 20)

        return goal
