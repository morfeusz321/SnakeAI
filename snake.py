import pygame
import settings
import copy

class Snake:
    def __init__(self):
        self.size = 10
        self.length = 1
        self.elements = [[settings.START_X, settings.START_Y]]
        self.before_move = copy.deepcopy(self.elements)
        self.direction = 'up'
        self.speed = settings.SNAKE_SPEED

    def draw(self, screen):
        for element in self.elements:
            pygame.draw.rect(screen, settings.GREEN, pygame.Rect(element[0], element[1], self.size, self.size))

    def move(self):
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
            self.elements[i] = copy.deepcopy(self.before_move[i-1])

    def game_over(self):
        # Check if the snake has hit the boundaries
        if (self.elements[0][0] < 0 or self.elements[0][0] >= settings.WIDTH or
            self.elements[0][1] < 0 or self.elements[0][1] >= settings.HEIGHT):
            return True
        # Check if the snake has hit itself
        if self.elements[0] in self.elements[1:]:
            return True
        return False

    def eats(self, food):
        if pygame.Rect(self.elements[0][0], self.elements[0][1], self.size, self.size).colliderect(
            pygame.Rect(food.position[0], food.position[1], food.size, food.size)):
            self.elements.append(list(self.before_move[-1]))  # Add a new element to the snake
            return True
        return False