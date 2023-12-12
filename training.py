import pygame

import math

import settings
from agent.agent import Agent
from agent.state import get_state
from agent.helper import plot
from game.snake import Snake


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

        change_game_speed()

        state_old = get_state(game)

        final_move = agent.get_action(state_old)

        move = translate_direction_to_input(final_move, game)

        reward, done, score = game.change_direction(move)

        state_new = get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)
        update_ui(game, screen)
        if done:
            # train long memory, plot result
            game = Snake()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            _plot_scores(agent, plot_mean_scores, plot_scores, score, total_score)


def _plot_scores(agent, plot_mean_scores, plot_scores, score, total_score):
    plot_scores.append(score)
    total_score += score
    mean_score = total_score / agent.n_games
    plot_mean_scores.append(mean_score)
    plot(plot_scores, plot_mean_scores)


def update_ui(game, screen):
    screen.fill(settings.WHITE)
    game.draw(screen)
    game.food.draw(screen)
    # Update display
    pygame.display.flip()


def translate_direction_to_input(final_move, game):
    if game.direction == 'up':
        move = 'left' if final_move[0] else 'up' if final_move[1] else 'right'
    elif game.direction == 'down':
        move = 'right' if final_move[0] else 'down' if final_move[1] else 'left'
    elif game.direction == 'left':
        move = 'down' if final_move[0] else 'left' if final_move[1] else 'up'
    else:
        move = 'up' if final_move[0] else 'right' if final_move[1] else 'down'
    return move


def change_game_speed():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:
                settings.SPEED *= 2
            elif event.key == pygame.K_MINUS:
                if settings.SPEED > 10:
                    settings.SPEED = math.floor(settings.SPEED // 2)
            elif event.key == pygame.K_r:
                settings.SPEED = 40


if __name__ == '__main__':
    train()
