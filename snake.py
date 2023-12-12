from typing import List

import pygame
import settings
import copy

from food import Food

pygame.font.init()


class Snake:
    def __init__(self):
        start_x = settings.WIDTH // 2
        start_y = settings.HEIGHT // 2
        self.size = settings.SNAKE_SIZE
        self.length = 1
        self.elements = [[start_x, start_y],
                         [start_x, start_y - self.size],
                         [start_x, start_y - 2 * self.size]]
        self.before_move = copy.deepcopy(self.elements)
        self.direction = 'up'
        self.score = 0
        self.speed = settings.SNAKE_SIZE
        self.food = Food(self.elements)
        self.frame_iteration = 0
        self.font = pygame.font.SysFont('arial', 20)

    def draw(self, screen):
        for element in self.elements:
            pygame.draw.rect(screen, settings.GREEN, pygame.Rect(element[0], element[1], self.size, self.size))

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        speed_text = self.font.render(f"Speed: {settings.SPEED}", True, (0, 0, 0))
        screen.blit(score_text, (settings.WIDTH - score_text.get_width(), 10))
        screen.blit(speed_text, (settings.WIDTH - speed_text.get_width(), 30))

    def change_direction(self, direction):
        self.direction = direction
        self.move()
        game_over = False
        reward = 0
        if self.frame_iteration > 100 * len(self.elements):
            game_over = True
            reward = -20
            return reward, game_over, self.score
        elif self.game_over(self.elements[0]):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if self.eats():
            self.score += 1
            reward = 10
            self.food = Food(self.elements)
        return reward, game_over, self.score

    def move(self):
        self.frame_iteration += 1
        # Copy current elements before they are updated
        self.before_move = copy.deepcopy(self.elements)

        # Move the head
        if self.direction == 'up':
            self.elements[0][1] -= self.speed
        elif self.direction == 'down':
            self.elements[0][1] += self.speed
        elif self.direction == 'left':
            self.elements[0][0] -= self.speed
        elif self.direction == 'right':
            self.elements[0][0] += self.speed

        # Move the rest of the body
        for i in range(1, len(self.elements)):
            self.elements[i] = copy.deepcopy(self.before_move[i - 1])

    def game_over(self, point: List[int]):
        # Check if the snake has hit the boundaries
        if (point[0] < 0 or point[0] >= settings.WIDTH or
                point[1] < 0 or point[1] >= settings.HEIGHT):
            return True
        # Check if the snake has hit itself
        if point in self.elements[1:]:
            return True
        return False

    def eats(self):
        if pygame.Rect(self.elements[0][0], self.elements[0][1], self.size, self.size).colliderect(
                pygame.Rect(self.food.position[0], self.food.position[1], self.food.size, self.food.size)):
            self.elements.append(list(self.before_move[-1]))  # Add a new element to the snake
            return True
        return False
