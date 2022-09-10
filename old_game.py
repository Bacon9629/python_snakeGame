import pygame
import copy
from parameter import Parameter
from ori_snake import OriSnake
from long_snake import LongSnake
from alert import Alert
from goal import Goal
from state import State

class Main(Parameter):
    def __init__(self):
        super().__init__()
        """初始化pygame"""
        pygame.init()
        """預設方向"""
        self.direction = 'down'
        """分數"""
        self.score = 0
        """建立蛇"""
        self.snake = OriSnake()
        self.snake_list = self.snake.create_body()
        """目標"""
        self.goal = Goal().get_goal(self.snake_list)
        """建立視窗"""
        self.win_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Snake Game")
        """state"""
        self.state = State()

    def run(self):
        """設定偵數"""
        fpsClock = pygame.time.Clock()
        """顯示分數"""
        scoreFont = pygame.font.Font(None, 65)

        while True:
            snake_old_location = copy.deepcopy(self.snake_list[0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            """按鍵偵測"""
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] and self.direction != 'right'):
                self.direction = 'left'
            if (keys[pygame.K_RIGHT] and self.direction != 'left'):
                self.direction = 'right'
            if (keys[pygame.K_UP] and self.direction != 'down'):
                self.direction = 'up'
            if (keys[pygame.K_DOWN] and self.direction != 'up' or self.direction == 'down'):
                self.direction = 'down'

            """改變座標"""
            if(self.direction == 'left'):
                self.snake_list[0].x -= self.snake.step
            elif(self.direction == 'right'):
                self.snake_list[0].x += self.snake.step
            elif(self.direction == 'up'):
                self.snake_list[0].y -= self.snake.step
            elif(self.direction == 'down'):
                self.snake_list[0].y += self.snake.step

            """state"""
            self.state.danger_state(snake_list=self.snake_list, direction=self.direction)
            self.state.direction_state(direction=self.direction)
            self.state.food_state(snake_list=self.snake_list, food_loc=self.goal)
            print(self.state.get_state())

            """判斷是否碰到自己"""
            if (self.snake_list[0] in self.snake_list[1:]):
                self.restart_game()
                continue

            """判斷是否撞到邊界"""
            if (self.snake_list[0].x < 0 or self.snake_list[0].x > self.win_width or self.snake_list[0].y < 0 or self.snake_list[0].y > self.win_height):
                self.restart_game()
                continue

            """判斷有沒有吃到獎勵"""
            if(pygame.Rect.colliderect(self.snake_list[0],self.goal)):
                self.snake_list = self.snake.add_body(snake_old_location, self.snake_list)
                self.goal = Goal().get_goal(self.snake_list)
                self.score += 1
            else:
                self.snake_list = self.snake.move_body(self.snake_list, snake_old_location)


            """繪製"""
            self.win_screen.fill((0, 0, 0))
            for snake in self.snake_list:
                pygame.draw.rect(self.win_screen,self.snake.color,snake)
            pygame.draw.rect(self.win_screen, (255, 0, 0), self.goal)
            self.scoreFontSurf = scoreFont.render(f'score {self.score}', True, (255, 255, 255))
            self.scoreFontRect = self.scoreFontSurf.get_rect()
            self.scoreFontRect.topleft = (20,20)
            self.win_screen.blit(self.scoreFontSurf, self.scoreFontRect)

            pygame.display.update()
            fpsClock.tick(8)

        pygame.quit()

    def restart_game(self):
        Alert().game_over(self.win_screen,self.score)
        self.direction = 'down'
        self.snake_list = self.snake.create_body()
        self.goal = Goal().get_goal(self.snake_list)
        self.score = 0


if __name__ == '__main__':
    main = Main()
    main.run()
