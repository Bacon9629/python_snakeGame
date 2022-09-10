import pygame
import copy
from RL_train import RL
from parameter import Parameter
from ori_snake import OriSnake
from alert import Alert
from goal import Goal
from state import State
import threading
import matplotlib.pyplot as plot


class Main(Parameter):
    def __init__(self):
        super().__init__()
        """初始化pygame"""
        pygame.init()
        """預設方向"""
        self.direction = 'down'
        """建立蛇"""
        self.snake = OriSnake()
        self.snake_list = self.snake.create_body()
        """目標"""
        self.goal = Goal().get_goal(self.snake_list)
        """State"""
        self.state = State()
        """RL"""
        self.rl = RL()
        """建立視窗"""
        self.win_screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Snake Game")

        self.slow = False

        self.y = []
        self.x = []

        self.finish = False

    def set_slow(self, is_slow):
        self.slow = is_slow


    def run(self):
        """設定偵數"""
        fpsClock = pygame.time.Clock()
        """Train"""
        max = 1
        epoch = 0
        all_score = [0 for _ in range(0, 20)]
        # for epoch in range(1000):
        while True:
            epoch += 1
            self.restart_game()
            while True:

                pygame.event.get()

                snake_old_location = copy.deepcopy(self.snake_list[0])

                """get action"""
                old_state = self.generator_state()
                self.rl.add_state(old_state)
                action = self.rl.train_action(old_state)

                """parse action"""
                if(action == 0):
                    pass
                elif(action == 1):
                    if(self.direction == 'up'):
                        self.direction = 'right'
                    elif(self.direction == 'down'):
                        self.direction = 'left'
                    elif(self.direction == 'left'):
                        self.direction = 'up'
                    elif(self.direction == 'right'):
                        self.direction = 'down'
                elif(action == 2):
                    if (self.direction == 'up'):
                        self.direction = 'left'
                    elif(self.direction == 'down'):
                        self.direction = 'right'
                    elif (self.direction == 'left'):
                        self.direction = 'down'
                    elif (self.direction == 'right'):
                        self.direction = 'up'

                """改變座標"""
                if(self.direction == 'left'):
                    self.snake_list[0].x -= self.snake.step
                elif(self.direction == 'right'):
                    self.snake_list[0].x += self.snake.step
                elif(self.direction == 'up'):
                    self.snake_list[0].y -= self.snake.step
                elif(self.direction == 'down'):
                    self.snake_list[0].y += self.snake.step

                """移動body"""

                """判斷有沒有吃到獎勵"""
                if(pygame.Rect.colliderect(self.snake_list[0],self.goal)):
                    self.snake_list = self.snake.add_body(snake_old_location, self.snake_list)
                    self.goal = Goal().get_goal(self.snake_list)
                    reward = 500
                    self.update_q_table(old_state=old_state, reward=reward)
                else:
                    self.snake_list = self.snake.move_body(self.snake_list, snake_old_location)
                    reward = -5
                    self.update_q_table(old_state=old_state, reward=reward)

                """判斷是否碰到自己"""
                if (self.snake_list[0] in self.snake_list[1:]):
                    reward = -300
                    self.update_q_table(old_state=old_state,reward=reward)
                    break

                """判斷是否撞到邊界"""
                if (self.snake_list[0].x < 0 or self.snake_list[0].x == self.win_width or self.snake_list[0].y < 0 or self.snake_list[0].y == self.win_height):
                    reward = -200
                    self.update_q_table(old_state=old_state, reward=reward)
                    break

                """判斷現在與周遭身體的前進方向是否相同"""
                if len(self.snake_list) > 10:
                    if self.wrong_direction(self.snake_list, self.direction):
                        reward -= 80
                        self.update_q_table(old_state=old_state, reward=reward)

                """繪製"""
                # if(epoch > 500):
                if (self.slow):

                    self.win_screen.fill((0, 0, 0))
                    for snake in self.snake_list:
                        pygame.draw.rect(self.win_screen,self.snake.color,snake)
                    pygame.draw.rect(self.win_screen, (255, 0, 0), self.goal)

                    pygame.display.update()
                    fpsClock.tick(100)

            if(len(self.snake_list) > max):
                max = len(self.snake_list)

            all_score[epoch % 20] = len(self.snake_list)

            average = int(sum(all_score) / len(all_score))
            self.y.append(average)
            self.x.append(epoch)

            self.rl.adjust_hyperparameter(epoch)

            print('Train times:', epoch, "  now score: ", len(self.snake_list))
            print('Best score:', max, "  average: ", average)

            if epoch > 1100:
                self.rl.save_q_table()
                self.finish = True
                break

    def wrong_direction(self, snake_list, direction):
        head_xy = (snake_list[0][0], snake_list[0][1])
        detect_body_xy_list = [
            (head_xy[0] - 20, head_xy[1]),
            (head_xy[0] + 20, head_xy[1]),
            (head_xy[0], head_xy[1] - 20),
            (head_xy[0], head_xy[1] + 20)
        ]

        remove_item = (snake_list[1][0], snake_list[1][1])
        detect_body_xy_list.remove(remove_item)

        index_list = []  # 被碰到的身體的索引值
        # for item in detect_body_xy_list:
        for index, snake_body in enumerate(snake_list):
            if (snake_body[0], snake_body[1]) in detect_body_xy_list:
                index_list.append(index)

        violate_dir_list = [self.get_body_move_direction(snake_list, i) for i in index_list]
        if direction in violate_dir_list:
            return True
        else:
            return False

    def get_body_move_direction(self, snake_list: list, body_index: int) -> str:
        result = "none"
        if len(snake_list) < 3:
            raise ValueError("身體長度太短，無法判斷方向")

        me = snake_list[body_index]
        if body_index != 1:
            front_of_me = snake_list[body_index - 1]
            if front_of_me.x > me.x:
                result = 'right'
            elif front_of_me.x < me.x:
                result = 'left'
            if front_of_me.y > me.y:
                result = 'down'
            elif front_of_me.y < me.y:
                result = 'up'
        else:
            back_of_me = snake_list[body_index + 1]
            if back_of_me.x < me.x:
                result = 'right'
            elif back_of_me.x > me.x:
                result = 'left'
            if back_of_me.y < me.y:
                result = 'down'
            elif back_of_me.y > me.y:
                result = 'up'

        return result


    def update_q_table(self,old_state,reward):
        new_state = self.generator_state()
        self.rl.add_state(new_state)
        self.rl.update_q_tabel(old_state, new_state, reward)

    def generator_state(self) -> list:
        self.state.danger_state(snake_list=self.snake_list, direction=self.direction)
        self.state.direction_state(direction=self.direction)
        self.state.food_state(snake_list=self.snake_list, food_loc=self.goal)
        self.state.wrong_direction(self.snake_list, self.direction)

        return self.state.get_state()

    def restart_game(self):
        self.direction = 'down'
        self.snake_list = self.snake.create_body()
        self.goal = Goal().get_goal(self.snake_list)


if __name__ == '__main__':

    def t(main):
        while True:
            input()
            main.set_slow(not main.slow)
            print("\n" + "change" + "\n")

    main = Main()

    train_thread = threading.Thread(target=t, args=(main,))
    train_thread.start()

    main.run()

    while(not main.finish):
        pass

    plot.plot(main.x, main.y)
    plot.show()





