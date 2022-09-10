import pygame
from snake import Snake
from parameter import Parameter


pygame.init()

class OriSnake(Parameter,Snake):
    def __init__(self):
        super().__init__()
        """蛇的參數"""
        self.__color = (125,125,125)
        self.__step = 20
        self.__width = 20

    @property
    def color(self):
        return self.__color

    @property
    def step(self):
        return self.__step

    @property
    def width(self):
        return self.__width

    """創建蛇"""
    def create_body(self) -> list:
        x = int((self.win_width - self.__width) / 2)
        y = int((self.win_height - self.__width) / 2)
        snake_head = pygame.Rect(x, y, self.__width, self.__width)

        return [snake_head]

    """增加身體長度"""
    def add_body(self,snake_old_location,snake_list) -> list:
        snake_list.insert(1,snake_old_location)
        return snake_list

    """移動身體"""
    def move_body(self,snake_list,snake_old_location) -> list:
        if(len(snake_list) > 1):
            snake_list.insert(1, snake_old_location)
            snake_list.pop()

        return snake_list

