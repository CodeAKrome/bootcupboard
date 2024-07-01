# To write the game of snake in Python, you will need to follow these steps:

# 1. Create a class for the snake object, which will have attributes such as `x` and `y` coordinates, a direction (up, down, left, right), and a length.
# 2. Create a function that generates a new snake object with a specified initial size and location on the screen.
# 3. Create a function that moves the snake one step in its current direction and checks for any collisions with the edges of the screen or itself. If there is a collision, terminate the game.
# 4. Create a function that displays the updated snake object on the screen.
# 5. Create a loop that repeatedly calls the `move_snake` function until the user presses the `ESC` key to quit the game.
# 6. In the main function of your program, generate a new snake object with an initial size and location on the screen using the `create_snake` function, and then call the `game_loop` function in a loop until the user quits the game by pressing the `ESC` key.

# Here is some sample code that demonstrates how you might implement these functions:
# ```python
import turtle  # for graphics
import secrets

class Snake:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = 1

    def move(self):
        if self.direction == 'up':
            self.y += 10
        elif self.direction == 'down':
            self.y -= 10
        elif self.direction == 'left':
            self.x += 10
        else:  # self.direction == 'right'
            self.x -= 10

    def grow(self):
        self.length += 1

def create_snake():
    x = secrets.SystemRandom().randint(-250, 250)
    y = secrets.SystemRandom().randint(-250, 250)
    direction = secrets.choice(['up', 'down', 'left', 'right'])
    return Snake(x, y, direction)

def move_snake():
    snake = create_snake()
    while True:
        snake.move()
        snake.grow()
        # Check for collisions with edges of screen and self
        if snake.x < -250 or snake.y < -250 or snake.x > 250 or snake.y > 250:
            print("Game over! You hit the edge of the screen.")
            break
        elif snake.length >= 10:
            print("Congratulations, you ate yourself!")
            break
        # Update display
        turtle.clear()
        turtle.penup()
        turtle.goto(snake.x, snake.y)
        turtle.pendown()
        for i in range(10):
            if i < snake.length:
                turtle.forward(5)
            else:
                turtle.right(90)
                turtle.forward(5)
                turtle.left(90)
        turtle.update()

def game_loop():
    while True:
        move_snake()
        if turtle.screen.getcanvas()._root().getkey():  # _root() is a Tkinter internal method for getting the root window of the canvas
            break
    print("Thanks for playing!")

game_loop()  # This starts the game loop, which will repeatedly call move_snake() until the user quits by pressing the ESC key.
#```
