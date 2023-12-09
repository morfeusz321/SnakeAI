import pygame
import settings
import random


class Food:
    def __init__(self, snake_positions):
        self.size = settings.FOOD_SIZE
        self.color = settings.RED
        self.position = self.generate_position(snake_positions)

    def generate_position(self, snake_positions):
        while True:
            position = [random.randint(0, (settings.WIDTH // self.size) - 1) * self.size,
                        random.randint(0, (settings.HEIGHT // self.size) - 1) * self.size]
            if position not in snake_positions:
                return position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.size, self.size))
