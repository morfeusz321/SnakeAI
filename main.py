import pygame
import settings
from game.snake import Snake
from game.food import Food

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

# Create a snake object and a food object
snake = Snake()

# Create a clock object
clock = pygame.time.Clock()

# Game loop
running = True


def update_ui():
    screen.fill(settings.WHITE)
    snake.draw(screen)
    snake.food.draw(screen)
    # Update display
    pygame.display.flip()


while running:
    # Cap the maximum speed
    clock.tick(settings.SPEED)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = 'up'
            elif event.key == pygame.K_DOWN:
                snake.direction = 'down'
            elif event.key == pygame.K_LEFT:
                snake.direction = 'left'
            elif event.key == pygame.K_RIGHT:
                snake.direction = 'right'

    # Update snake
    snake.move()

    # Check if snake has eaten the food
    if snake.eats():
        snake.length += 1
        snake.food = Food(snake.elements)

    # Check if game over
    if snake.game_over(snake.elements[0]):
        print("Game Over!")
        running = False

    # Draw everything
    update_ui()

# Quit Pygame
pygame.quit()
