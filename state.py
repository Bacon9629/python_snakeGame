from parameter import Parameter
import copy

class State(Parameter):
    def __init__(self):
        super().__init__()
        self.state_list = [False]*12
        """
            [0]danger straight
            [1]danger right
            [2]danger left
            [3]direction up
            [4]direction down
            [5]direction left
            [6]direction right
            [7]food up
            [8]food down
            [9]food left
            [10]food right
            [11]現在與周遭身體的前進方向相同 wrong_direction
        """
    def danger_state(self,snake_list,direction):
        head_copy = []
        for i in range(4):
            head_copy.append(copy.deepcopy(snake_list[0]))

        head_copy[0].y -= 20
        head_copy[1].y += 20
        head_copy[2].x -= 20
        head_copy[3].x += 20

        if(direction == 'up'):
            if(snake_list[0].y == 0):
                self.state_list[0] = True
            if(head_copy[0] in snake_list):
                self.state_list[0] = True
            if(snake_list[0].x == self.win_width - 20):
                self.state_list[1] = True
            if(head_copy[3] in snake_list):
                self.state_list[1] = True
            if(snake_list[0].x == 0):
                self.state_list[2] = True
            if(head_copy[2] in snake_list):
                self.state_list[2] = True

        elif(direction == 'down'):
            if(snake_list[0].y == self.win_height - 20):
                self.state_list[0] = True
            if(head_copy[1] in snake_list):
                self.state_list[0] = True
            if(snake_list[0].x == 0):
                self.state_list[1] = True
            if(head_copy[2] in snake_list):
                self.state_list[1] = True
            if(snake_list[0].x == self.win_width - 20):
                self.state_list[2] = True
            if(head_copy[3] in snake_list):
                self.state_list[2] = True

        elif(direction == 'left'):
            if(snake_list[0].x == 0):
                self.state_list[0] = True
            if(head_copy[2] in snake_list):
                self.state_list[0] = True
            if(snake_list[0].y == 0):
                self.state_list[1] = True
            if(head_copy[0] in snake_list):
                self.state_list[1] = True
            if(snake_list[0].y == self.win_height - 20):
                self.state_list[2] = True
            if(head_copy[1] in snake_list):
                self.state_list[2] = True

        elif(direction == 'right'):
            if(snake_list[0].x == self.win_width - 20):
                self.state_list[0] = True
            if(head_copy[3] in snake_list):
                self.state_list[0] = True
            if(snake_list[0].y == self.win_height - 20):
                self.state_list[1] = True
            if(head_copy[1] in snake_list):
                self.state_list[1] = True
            if(snake_list[0].y == 0):
                self.state_list[2] = True
            if(head_copy[0] in snake_list):
                self.state_list[2] = True

    def direction_state(self,direction):
        if(direction == 'up'):
            self.state_list[3] = True
        elif(direction == 'down'):
            self.state_list[4] = True
        elif(direction == 'left'):
            self.state_list[5] = True
        elif(direction == 'right'):
            self.state_list[6] = True

    # def danger_closed(self):


    def food_state(self,snake_list,food_loc):
        """food up"""
        if(snake_list[0].y > food_loc.y):
            self.state_list[7] = True
        """food down"""
        if(snake_list[0].y < food_loc.y):
            self.state_list[8] = True
        """food left"""
        if(snake_list[0].x > food_loc.x):
            self.state_list[9] = True
        """food right"""
        if(snake_list[0].x < food_loc.x):
            self.state_list[10] = True

    def get_state(self):
        state = self.state_list
        self.state_list = [False] * 12
        return state

    def wrong_direction(self, snake_list, direction):
        if len(snake_list) < 10:
            return
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
        for item in detect_body_xy_list:
            for index, snake_body in enumerate(snake_list):
                if item == (snake_body[0], snake_body[1]):
                    index_list.append(index)

        violate_dir_list = [self.get_body_move_direction(snake_list, i) for i in index_list]
        if direction in violate_dir_list:
            self.state_list[11] = True

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

