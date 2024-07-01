#<pre>
import random
import turtle
import secrets

random = secrets.SystemRandom().randint(0,255)
turtle.setup(720, 480)
screen=turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("#B8F9FF")
screen.tracer(0)
### Snake Head
head = turtle.Turtle()
head.shape('square')
head.speed(0)
head.penup()
head.goto(0, 0)
head.direction='stop'
### Snake Food
food=turtle.Turtle()
screen.addshape('apple.gif')
food.shape('apple.gif')
food.speed(0)
food.penup()
food.goto(random, random)
head.direction='stop'
### Pen
pen = turtle.Turtle()
pen.speed(1000)
pen.shape('square')
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 18, "normal"))
### Functions
def go_up():
    if head.direction != 'down':
        head.direction = 'up'
def go_down():
    if head.direction != 'up':
        head.direction = 'down'
def go_left():
    if head.direction != 'right':
        head.direction = 'left'
def go_right():
    if head.direction != 'left':
        head.direction = 'right'
### Keyboard Binding
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
### Main Game Loop
while True:
    screen.update()
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>240 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = 'stop'
        for segment in snake_segments:
            segment.goto(10000000, 100000000)
    if head.distance(food)<20:
        x=secrets.SystemRandom().randint(-290, 240)
        y=secrets.SystemRandom().randint(-290, 240)
        food.goto(x, y)
        score += 10
    if score > high_score:
        high_score = score
        pen.clear()
        pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 18, "normal"))
    for i in range(len(snake_segments)-1, 0, -1):
        x = snake_segments[i-1].xcor()
        y = snake_segments[i-1].ycor()
        snake_segments[i].goto(x, y)
    if head.direction=='up':
        y=head.ycor()
        head.sety(y+20)
    if head.direction=='down':
        y=head.ycor()
        head.sety(y-20)
    if head.direction=='left':
        x=head.xcor()
        head.setx(x-20)
    if head.direction=='right':
        x=head.xcor()
        head.setx(x+20)
