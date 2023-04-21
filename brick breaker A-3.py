import pgzrun
import time
import math
#the pygame simplifies the game development by providing API
#: The time module is part of the Python Standard Library and provides various functions to work with time. 
#: provides mathematical functions

TITLE = "Brickbreaker"
WIDTH = 640
HEIGHT = 480
BRICKS_PER_ROW = 10
# TITLE defines a variable called brickbreaker
# WIDTH defines the variable called width and assigns the integer value 640 to it.
# HEIGHT defines the variable height and assigns the integer value of 480 to it.
# BRICK PER ROW defines the variable rows and assigns the integer value of 10.

game_started = False
game_over = False
start_time = 0
timer = 1000
score = 0
# game started defines the variable game started and checks if the game is started or not
# game over defines the variable game over and checks if the game has ended or not
#start time keeps track of the start time of the game 
#timer is used as a count down variable 
# score is used to keep track of the score in the game

leaderboard = []

paddle = Actor("paddlered.png")
paddle.x = 320
paddle.y = 460
#leaderboard is a variable that keeps track of the previous scores in the game
# The paddle Actor represents a visual object on the screen 
#the paddle "x" and "y" represent the position of the paddle on the screen

ball = Actor("ballgrey.png")
ball.x = 320
ball.y = 320
ball_x_speed = 3
ball_y_speed = 3
ball_speed = 3
# the ball actor represents a visual object on the screen
# the ball "x""y" represents the intial position of the ball
# the ball x speed represents the horizontal speed of the ball
# the ball y speed represents the vertical speed of the ball
# the ball speed represents the overall speed of the ball

bricks = []
brick_sprites = ["element_green_rectangle.png", "element_yellow_rectangle.png", "element_red_rectangle.png"]

def draw():
    screen.fill((100, 149, 237))
    draw_elements()
    draw_messages()
#bricks variable basically stores the object that appears on the screen.
#brick sprites which has three variables respresnts the colour of the bricks in the game.
#The screen fill function fills the entire screen with colour
#The def draw function is used to update the frames 

def draw_elements():
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()
#this defines the image of paddle, ball and brick in the game and assumes that the necessary objects are created and methods are properly defined.

def draw_messages():
    screen.draw.text("Time: {}".format(timer), topright=(WIDTH-10, 10), fontsize=30, color="black")
    screen.draw.text("Score: {}".format(score), topleft=(WIDTH // 10, 10), fontsize=30, color="black")

    if not game_started:
        screen.draw.text("Press ENTER to start", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="orange")

    if game_over:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=30, color="red")
        screen.draw.text("Press ENTER to restart", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=30, color="white")
        draw_leaderboard()
#draw_messages(). This function appears to be responsible for drawing text-based messages on the game screen, such as the time, score, game start prompt, 
def draw_leaderboard():
    screen.draw.text("Leaderboard", topleft=(WIDTH // 4, HEIGHT // 5), fontsize=30, color="white")
    for i, entry in enumerate(leaderboard[:5]):
        screen.draw.text("{}. {}".format(i + 1, entry), topleft=(WIDTH // 4, HEIGHT // 5 + 40 * (i + 1)), fontsize=30, color="white")
#draw_leaderboard(). This function appears to be responsible for drawing a leaderboard displaying the top players' scores or rankings in the game.
def update():
    global game_started

    global game_over
    global start_time
    global timer

    if keyboard.RETURN and not game_started:
        game_started = True
        start_time = time.time()

    if game_started and not game_over:
        update_paddle()
        update_ball()

        elapsed_time = int(time.time() - start_time)
        timer = 1000 - elapsed_time
        if timer <= 0:
            game_over = True

    if game_over and keyboard.RETURN:
        add_to_leaderboard(score)
        reset_game()
#. This function appears to be responsible for updating the game state, handling keyboard input, and controlling game flow.

def update_paddle():
    if keyboard.a:
        if (paddle.x - 4 > + 52):
            paddle.x = paddle.x - 4
    if keyboard.d:
        if (paddle.x + 4 < 640 - 48):
            paddle.x = paddle.x + 4
#update_paddle(). This function appears to be responsible for updating the paddle's position based on keyboard inputs

def update_ball():
    global ball_x_speed
    global ball_y_speed
    global game_over
    global score

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    if(ball.x > WIDTH - 16) or (ball.x < 0):
        ball_x_speed = -ball_x_speed

    if ball.y < 0:
        ball_y_speed = -ball_y_speed

    if ball.y > HEIGHT - 16:
        game_over = True

    if ball.colliderect(paddle):
        ball_y_speed = -ball_y_speed
        relative_position = (ball.x - paddle.x) / (paddle.width / 2)
        angle = relative_position * 60
        ball_x_speed = ball_speed * math.sin(math.radians(angle))

    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_y_speed = -ball_y_speed
            score += 10
#this function is responsible for updatying the position of the ball in between the game.
#this determines the position of the ball based on the collision on the paddle, brick and the edges

def place_brick_row(sprite, pos_x, pos_y):
    for i in range(BRICKS_PER_ROW):
        brick = Actor(sprite)
        brick.x = pos_x + i * 64
        brick.y = pos_y
        bricks.append(brick)
#this function is responsible for placing the bricks in the game.
# #this takes 3 arguments 'sprite', 'pos x' and 'pos y'.
#'sprite' determines the image to be used for the bricks
#'pos x' and 'pos y' determines the initial co-ordinates of the row of bricks.

def reset_game():
    global game_started
    global game_over
    global timer
    global start_time
    global ball
    global bricks
    global score

    game_started = False
    game_over = False
    timer = 120
    score = 0
    ball.x = 320
    ball.y = 340
    bricks.clear()

    current_brick_pos_x = 64 / 2
    current_brick_pos_y = 32 / 2

    for brick_sprite in brick_sprites:
        for i in range(4):
            place_brick_row(brick_sprite, current_brick_pos_x, current_brick_pos_y)
            current_brick_pos_y += 32

    start_time = 0
#this function resets the game to its initial state
#it resets the position of the ball, the paddler and the number of bricks

def add_to_leaderboard(new_score):
    global leaderboard
    leaderboard.append(new_score)
    leaderboard.sort(reverse=True)

current_brick_pos_x = 64 / 2
current_brick_pos_y = 32 / 2

for brick_sprite in brick_sprites:
    for i in range(3):
        place_brick_row(brick_sprite, current_brick_pos_x, current_brick_pos_y)
        current_brick_pos_y += 32
#this function adds a new score to the global leaderboard list and sorts it in descending order.

pgzrun.go()
#this is typically the last piece in a pygame code.