import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
SPEED = 10
BLOCK_SIZE = 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the snake and food
snake = [(200, 200), (220, 200), (240, 200)]
food = (400, 300)

# Set up some variables to keep track of the game state
direction = 'right'
game_over = False

# Main game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'
            elif event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'

    # Move the snake
    head = snake[0]
    if direction == 'left':
        new_head = (head[0] - BLOCK_SIZE, head[1])
    elif direction == 'right':
        new_head = (head[0] + BLOCK_SIZE, head[1])
    elif direction == 'up':
        new_head = (head[0], head[1] - BLOCK_SIZE)
    else:
        new_head = (head[0], head[1] + BLOCK_SIZE)

    snake.insert(0, new_head)

    # Check for collisions with the food
    if snake[0] == food:
        food = (random.randint(0, WIDTH-BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT-BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
    else:
        snake.pop()

    # Check for collisions with the edge of the screen
    if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
        game_over = True

    # Check for collisions with the snake's own body
    for segment in snake[1:]:
        if snake[0] == segment:
            game_over = True

    # Draw everything
    screen.fill((255, 255, 255))
    for pos in snake:
        pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // SPEED)

# Quit Pygame
pygame.quit()
