import pygame
import random

# Define game constants
WIDTH = 500
HEIGHT = 500
FPS = 30
BLOCKSIZE = 20

# Initialize pygame and create a screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define snake position and direction
snake_x = WIDTH // 2
snake_y = HEIGHT // 2
direction = "right"

# Set up the snake list to represent its body
snake_list = []

# Create the apple object
apple_x = random.randint(0, int(WIDTH / BLOCKSIZE)) * BLOCKSIZE
apple_y = random.randint(0, int(HEIGHT / BLOCKSIZE)) * BLOCKSIZE

def create_snake():
    # Add first segment of the snake to the list
    snake_list.append(tuple([snake_x, snake_y]))
    # Create more segments for the body of the snake
    for _ in range(5):
        x = int(snake_x - BLOCKSIZE)
        y = int(snake_y)
        snake_list.append(tuple([x, y]))

def draw_snake():
    # Draw each segment of the snake
    for segment in reversed(snake_list):
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCKSIZE, BLOCKSIZE))

def draw_apple():
    # Create an apple using a rectangle
    pygame.draw.rect(screen, RED, pygame.Rect(apple_x, apple_y, BLOCKSIZE, BLOCKSIZE))

def game_over_text():
    # Write the Game Over text in red color on screen
    font = pygame.font.SysFont("comicsans", 75)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

def move():
    global apple_x, apple_y

    if direction == "right":
        snake_x += BLOCKSIZE
    elif direction == "left":
        snake_x -= BLOCKSIZE
    elif direction == "down":
        snake_y += BLOCKSIZE
    elif direction == "up":
        snake_y -= BLOCKSIZE

# Check if the head of the snake hits an edge or itself
def game_rules():
    head = snake_list[0]
    for segment in snake_list[1:]:
        if head == segment:
            return True
    # Check collisions with edges
    if head[0] < 0 or head[0] > WIDTH - BLOCKSIZE or head[1] < 0 or head[1] > HEIGHT - BLOCKSIZE:
        return True

# Check if the snake eats the apple
def eat_apple():
    if snake_list[0] == tuple([apple_x, apple_y]):
        # Generate new position for the apple
        apple_x = random.randint(0, int(WIDTH / BLOCKSIZE)) * BLOCKSIZE
        apple_y = random.randint(0, int(HEIGHT / BLOCKSIZE)) * BLOCKSIZE
        snake_list.insert(0, tuple([snake_x, snake_y]))

# Controls the direction of the snake
def controls():
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT] and direction != "right":
        direction = "left"
    elif key[pygame.K_RIGHT] and direction != "left":
        direction = "right"
    elif key[pygame.K_UP] and direction != "down":
        direction = "up"
    elif key[pygame.K_DOWN] and direction != "up":
        direction = "down"

def main():
    create_snake()
    
    running = True
    while running:
        
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                controls()

        screen.fill(WHITE)
        
        # Move the snake
        move()

        # Apply game rules
        if game_rules():
            draw_snake()
            game_over_text()
            running = False

        eat_apple()

        # Redraw everything on the screen
        draw_snake()
        draw_apple()
        
        pygame.display.update()
        
        clock = pygame.time.Clock()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
