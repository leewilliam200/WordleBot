from calendar import c
from pickle import NONE
from tkinter import scrolledtext
import torch
import random
import numpy as np
from collections import deque
from wordleAI import wordleGame
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.1

used = []
curr_iter = 0

class Agent:
    def __init__(self):
        self.no_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #popleft()
        self.model = Linear_QNet(15, 500, 100)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_state(self, game):
        state = game.state
        print(np.array(state, dtype=int))
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        global used
        global curr_iter
        #random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.no_games
        move = 0
        if curr_iter == 0:
            move = 95
            used.append(95)
            print("first")
        else:
            if random.randint(0, 200) < self.epsilon:
                move = int(random.randint(0, 99))
                used.append(move)
                print("random")
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)
                move = torch.argmax(prediction).item()
                moves = torch.topk(prediction, 5)
                print("prediction")
                print(move)
                print(moves)
                while move in used:
                    prediction[move] = -100
                    move = torch.argmax(prediction).item()
                used.append(move)
        print("""
        **********************
        """)
        curr_iter += 1
        if curr_iter == 7:
            curr_iter = 0
        return move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = wordleGame()
    while True:
        global used
        #get old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        #remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            #train long memory, plot result
            game.reset()
            agent.no_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.no_games, 'Score', score, 'Record', record)
            print('-------------', agent.no_games, '-----------------')
            print("""

            """)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.no_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            used = []

if __name__ == '__main__':
    train()