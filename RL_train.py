import numpy as np
import random
import pickle

class RL:
    def __init__(self):
        """Hyperparameters"""
        self.alpha = 0.3
        self.gamma = 0.6
        self.epsilon = 0.3
        """action_list = [straight 、 right 、 left]"""
        self.q_tabel = []
        self.state_list = []
        self.action = None

    """降低alpha、gamma、epsilon"""
    def adjust_hyperparameter(self, epoch):
        if epoch % 100 == 0:
            self.alpha *= 0.82
            self.gamma *= 0.82
            self.epsilon *= 0.3

    """新增狀態"""
    def add_state(self, state):
        if(state not in self.state_list):
            self.state_list.append(state)
            self.q_tabel.append([0,0,0])

    """訓練動作"""
    def train_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            self.action = random.choice([0,1,2])
        else:
            index = self.state_list.index(state)
            self.action = self.q_tabel[index].index(max(self.q_tabel[index]))

        return self.action

    """取得動作(已有q-table的值)"""
    def get_action(self, state):
        index = self.state_list.index(state)
        self.action = self.q_tabel[index].index(max(self.q_tabel[index]))

        return self.action

    """更新q-table"""
    def update_q_tabel(self, old_state, new_state, reward):
        old_state_index = self.state_list.index(old_state)
        old_value = self.q_tabel[old_state_index][self.action]

        next_state_index = self.state_list.index(new_state)
        next_max = max(self.q_tabel[next_state_index])

        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)

        self.q_tabel[old_state_index][self.action] = new_value


    """儲存q-table"""
    def save_q_table(self):
        file = open('Qvalue/q_table.txt', 'wb')
        pickle.dump(self.q_tabel,file)
        file.close()

    """讀取q-table"""
    def load_q_table(self):
        try:
            file = open('Qvalue/q_table.txt', 'rb')
            self.q_tabel = pickle.load(file)
            file.close()
        except:
            print('No Qvalue dir!')
