#[SYS]
# Importing modules
import pygame, sys, random
from pygame.locals import *

# Setting up constants
FPS = 30 # frames per second setting
WINDOWWIDTH = 640 # size of the window's width in pixels
WINDOWHEIGHT = 480 # size of the window's height in pixels
CELLSIZE = 20 # size of the grid cells in pixels
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE) # number of cells wide
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE) #number of cells high

# Colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

# Starting coordinates for initial block and apple
startx = random.randint(5, CELLWIDTH - 6)
starty = random.randint(5, CELLHEIGHT - 6)
apple_x = random.randint(0, CELLWIDTH - 1)
apple_y = random.randint(0, CELLHEIGHT - 1)

# Initializing the snake's direction and length
direction = RIGHT
length = 3

# Creating a list of blocked cells to initialize the snake
block_list = []
for i in range(length):
    block_list.append((startx - i, starty))

# Updating the snake's head and body coordinates
def update_block_positions():
    global block_list, length, direction
# EDIT
#    if len(block_list) &gt; length:
    if len(block_list) > length:
        del block_list[0]
    for i in range(len(block_list) - 1, 0, -1):
        block_list[i] = (block_list[i-1][0], block_list[i-1][1])
    if direction == UP:
        block_list[0] = (block_list[0][0], block_list[0][1] - 1)
    elif direction == DOWN:
        block_list[0] = (block_list[0][0], block_list[0][1] + 1)
    elif direction == LEFT:
        block_list[0] = (block_list[0][0] - 1, block_list[0][1])
    elif direction == RIGHT:
        block_list[0] = (block_list[0][0] + 1, block_list[0][1])

# Drawing the grid cells and snake blocks on the game window
def draw_grid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def draw_blocks():
    for block in block_list:
        x, y = block
        pygame.draw.rect(DISPLAYSURF, RED, (x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE))

# Checking if the snake has hit itself or gone off-screen
def check_for_block_loss():
    global block_list
    for block in block_list[1:]:
        if block_list[0] == block:
            return True
# EDIT
#    if block_list[0][0] &lt; 0 or block_list[0][0] >= CELLWIDTH or block_list[0][1] &lt; 0 or block_list[0][1] >= CELLHEIGHT:
    if block_list[0][0] < 0 or block_list[0][0] >= CELLWIDTH or block_list[0][1] < 0 or block_list[0][1] >= CELLHEIGHT:
        return True
    else:
        return False

# Checking if the snake has eaten an apple
def check_for_apple():
    global apple_x, apple_y, length
    if block_list[0] == (apple_x, apple_y):
        length += 1
        apple_x = random.randint(0, CELLWIDTH - 1)
        apple_y = random.randint(0, CELLHEIGHT - 1)

# Drawing the apple on the game window
def draw_apple():
    pygame.draw.rect(DISPLAYSURF, GREEN, (apple_x * CELLSIZE, apple_y * CELLSIZE, CELLSIZE, CELLSIZE))

# Main function to run the game
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    
    pygame.display.set_caption("Snake")
    
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
        
        update_block_positions()
        check_for_apple()
        
        DISPLAYSURF.fill(BGCOLOR)
        draw_grid()
        draw_blocks()
        draw_apple()
        
        if check_for_block_loss():
            terminate()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Function to terminate the game and exit the program
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
#[/SYS]<</INST>
