import pygame
import torch
import random
import numpy as np
from collections import deque

import settings
from helper import plot
from model import LinearQNet, QTrainer
from snake import Snake

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


def get_state(snake: Snake):
    head = snake.elements[0]
    one_element_length = settings.SNAKE_SIZE
    point_l = [head[0] - one_element_length, head[1]]
    point_r = [head[0] + one_element_length, head[1]]
    point_u = [head[0], head[1] - one_element_length]
    point_d = [head[0], head[1] + one_element_length]

    dir_l = snake.direction == 'left'
    dir_r = snake.direction == 'right'
    dir_u = snake.direction == 'up'
    dir_d = snake.direction == 'down'

    state = [
        # Danger straight
        (dir_r and snake.game_over(point_r)) or
        (dir_l and snake.game_over(point_l)) or
        (dir_u and snake.game_over(point_u)) or
        (dir_d and snake.game_over(point_d)),

        # Danger right
        (dir_u and snake.game_over(point_r)) or
        (dir_d and snake.game_over(point_l)) or
        (dir_l and snake.game_over(point_u)) or
        (dir_r and snake.game_over(point_d)),

        # Danger left
        (dir_d and snake.game_over(point_r)) or
        (dir_u and snake.game_over(point_l)) or
        (dir_r and snake.game_over(point_u)) or
        (dir_l and snake.game_over(point_d)),

        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,

        # Food location
        snake.food.position[0] < head[0],  # food left
        snake.food.position[0] > head[0],  # food right
        snake.food.position[1] < head[1],  # food up
        snake.food.position[1] > head[1]  # food down
    ]

    return np.array(state, dtype=int)


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        # start with random moves and as epsilon decreases, start using the model
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Snake()
    clock = pygame.time.Clock()

    # Create game window
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    while True:
        clock.tick(settings.SPEED)
        # get old state
        state_old = get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # set move direction based on final_move and current direction
        if game.direction == 'up':
            move = 'left' if final_move[0] else 'up' if final_move[1] else 'right'
        elif game.direction == 'down':
            move = 'right' if final_move[0] else 'down' if final_move[1] else 'left'
        elif game.direction == 'left':
            move = 'down' if final_move[0] else 'left' if final_move[1] else 'up'
        elif game.direction == 'right':
            move = 'up' if final_move[0] else 'right' if final_move[1] else 'down'

        # move = 'left' if final_move[0] else 'up' if final_move[1] else 'right' if final_move[2] else 'down'
        # perform move and get new state
        reward, done, score = game.change_direction(move)
        state_new = get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        screen.fill(settings.WHITE)
        game.draw(screen)
        game.food.draw(screen)
        # Update display
        pygame.display.flip()
        if done:
            # train long memory, plot result
            game = Snake()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
