import numpy as np

import settings
from game.snake import Snake


def get_state(snake: Snake):
    head = snake.elements[0]
    one_element_length = settings.SNAKE_SIZE
    point_d, point_l, point_r, point_u = get_head_position_after_all_possible_moves(head, one_element_length)

    dir_d, dir_l, dir_r, dir_u = encode_current_direction(snake)

    state = [
        # Danger straight
        get_danger(dir_d, dir_l, dir_r, dir_u, point_d, point_l, point_r, point_u, snake),

        # Danger right
        get_danger(dir_r, dir_d, dir_u, dir_l, point_d, point_l, point_r, point_u, snake),

        # Danger left
        get_danger(dir_l, dir_u, dir_d, dir_r, point_d, point_l, point_r, point_u, snake),

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


def get_danger(dir_d, dir_l, dir_r, dir_u, point_d, point_l, point_r, point_u, snake):
    return (dir_r and snake.game_over(point_r)) or (dir_l and snake.game_over(point_l)) or (
                dir_u and snake.game_over(point_u)) or (dir_d and snake.game_over(point_d))


def encode_current_direction(snake):
    dir_l = snake.direction == 'left'
    dir_r = snake.direction == 'right'
    dir_u = snake.direction == 'up'
    dir_d = snake.direction == 'down'
    return dir_d, dir_l, dir_r, dir_u


def get_head_position_after_all_possible_moves(head, one_element_length):
    point_l = [head[0] - one_element_length, head[1]]
    point_r = [head[0] + one_element_length, head[1]]
    point_u = [head[0], head[1] - one_element_length]
    point_d = [head[0], head[1] + one_element_length]
    return point_d, point_l, point_r, point_u
