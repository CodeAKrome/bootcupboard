import pygame, sys, random

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (204, 0, 0)

# initialize pygame and set window size
pygame.init()
window_size = [600, 600]
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake Game")

# define game variables
clock = pygame.time.Clock()
snake_pos = [100, 50]
snake_body = []
direction = "RIGHT"
food_pos = [random.randrange(1, window_size[0]//10)*10, random.randrange(1, window_size[1]//10)*10]
score = 0

# create the snake body from the initial position
snake_body.append(snake_pos[:])

# game loop
while True:
    # handle user inputs (keyboard)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"

    # move the snake head according to the given direction
    if direction == "RIGHT":
        snake_pos[0] += 10
    elif direction == "LEFT":
        snake_pos[0] -= 10
    elif direction == "UP":
        snake_pos[1] -= 10
    elif direction == "DOWN":
        snake_pos[1] += 10

    # check if the head of the snake collides with its body
    for block in snake_body:
        if snake_pos == block:
            sys.exit()

    # add the new position to the snake's body and remove the tail (last element)
    snake_body.insert(0, snake_pos[:])
    if len(snake_body) > score + 1:
        del snake_body[-1]

    # check if the snake collides with the food or its own body
    if snake_pos == food_pos:
        food_pos = [random.randrange(1, window_size[0]//10)*10, random.randrange(1, window_size[1]//10)*10]
        score += 1
    else:
        snake_body.pop()

    # draw the game elements (food and snake) on the screen
    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.circle(screen, RED, food_pos, 5)
    font = pygame.font.SysFont('calibri', 40)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, [0, 0])
    pygame.display.flip()

    # limit the frame rate to 12 frames per second
    clock.tick(12)
