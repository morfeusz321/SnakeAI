import pygame
import settings
from snake import Snake
from food import Food

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

# Create a snake object and a food object
snake = Snake()
# Create a food object
food = Food(snake.elements)

# Create a clock object
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Cap the maximum speed at 10 frames per second
    clock.tick(settings.FPS)

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
    if snake.eats(food):
        snake.length += 1
        food = Food(snake.elements)

    # Check if game over
    if snake.game_over():
        print("Game Over!")
        running = False

    # Draw everything
    screen.fill(settings.WHITE)
    snake.draw(screen)
    food.draw(screen)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()