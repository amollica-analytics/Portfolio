#Anthony Mollica
#CS-140
#Assignment 3

#Create a video game where a ball bounces off a paddle and score is kept
import color
import pygame
import pygame_helper
import random

def move(x,y,dx,dy,dt):
    """
    Move the ball given a position and a velocity
    :param x: x-position
    :param y: y-position
    :param dx: x-velocity
    :param dy: y-velocity
    :param dt: time elapsed
    :return: (updated x, updated y, updated dx, updated dy)
    """
    #move the ball
    x=x+dx*dt
    y=y+dy*dt
    # check if the ball has touched bottom side or left side of the barrier
    if barrier_x <= x+ball_width<= barrier_x +barrier_width and barrier_y <=y<= barrier_y+barrier_height:
        #use sum to decide which
        wy=(ball_width+barrier_width)*((y-ball_height//2)-(barrier_y+barrier_height//2))
        hx=(ball_height+barrier_height)*((x+ball_width//2)-(barrier_x+barrier_width//2))

        if wy > hx:
            if wy > -hx:
                # ball hit the bottom
                y = barrier_y + barrier_height
                # change y direction of the ball
                dy = -dy
            else:
                # ball hit the left side
                x = barrier_x - ball_width
                # change x direction of the ball
                dx = -dx
    # did we hit the right side or top of the barrier
    if y > barrier_y - ball_height and barrier_x <= x <= barrier_x + barrier_width:
        # use Minkowski sum to determine which side of the barrier the ball hit
        wy = (ball_width + barrier_width) * ((y - ball_height // 2) - (barrier_y + barrier_height // 2))
        hx = (ball_height + barrier_height) * ((x + ball_width // 2) - (barrier_x + barrier_width // 2))
        if wy < hx:
            if wy > -hx:
                # ball hit the right side
                x = barrier_x + barrier_width
                # change the x direction of the ball
                dx = -dx
            else:
                # ball hit the top
                y = barrier_y - ball_height
                # change the y direction of the ball
                dy = -dy

    # did we hit the paddle or the right side wall?
    if x < paddle_x + paddle_width and paddle_y <= y + ball_height // 2 <= paddle_y + paddle_height:
        # vertical position to line up with the paddle
        # horizontal position to line up with the paddle
        x = paddle_x + paddle_width
        dx = -dx
    elif x + ball_width >= width:
        # right wall
        x = width - ball_width
        dx = -dx

    # did we hit a top or bottom wall
    if y < 0:
        # top wall
        y = 0
        dy = -dy
    elif y + ball_height >= height:
        # bottom wall
        y = height - ball_height
        dy = -dy

    return (x, y, dx, dy)

#Main Program
print("Welcome to pong!")
print("The rules:")
print("You will be rewarded a point each time ball touches the paddle.")
print("Ball will increase in velocity each time the ball hits the paddle.")
print("Try to not let the ball hit the left side of the wall, if you do, you lose.")
pygame.init()
# create a font
font = pygame.font.SysFont("Veranda", 30)

# tell pygame to repeat the key presses
pygame.key.set_repeat(1, 10)

height = 500
width= 600
win = pygame.display.set_mode((width, height))

win.fill(color.sky_blue)
# load image of the ball
ball = pygame.image.load("ball.png").convert_alpha()

# ball is a reference to a surface object that contains
# all of the pixel information from the image file
ball_width = ball.get_width()
ball_height = ball.get_height()

# load image of the paddle
paddle = pygame.image.load("paddle.png").convert_alpha()
paddle_width = paddle.get_width()
paddle_height = paddle.get_height()

# shift the paddle in 5 pixels from left
paddle_x = 5
paddle_y = width//2-paddle_height // 2

# move paddle 10 pixels up and down
paddle_dy = 8

#random choose location for ball to start
ball_x = random.randrange(10 + paddle_width, width // 5)
ball_y = random.randrange(height - ball_height)
# set initial velocity of ball
# random starting velocity for the ball
dx = ball_width // random.randrange(2,5)
dy = -ball_height //random.randrange(2,5)

pygame_helper.wait_for_click()

# create a stopwatch in pygame
clock = pygame.time.Clock()
# create a score
score = 0
msg = font.render("Score: " + str(score), True, color.black)
msg_width = msg.get_width()
msg_height = msg.get_height()
mouse_x,mouse_y=pygame.mouse.get_pos()

#loop for win or loss
done=False
while not done:
    #make window
    win.fill(color.aqua)
    #create line in middle
    pygame.draw.line(win,color.white,(width//2,0), (width//2, height), 8)
    #create a barrier in middle
    barrier_width= width // 5
    barrier_height = height // 4
    barrier_x = width // 2 - barrier_width// 2
    barrier_y = height // 2 - barrier_height // 2
    pygame.draw.rect(win, color.burntsienna, (barrier_x, barrier_y, barrier_width, barrier_height))

    #if user won
    if score==10:
        msg1 = font.render("WINNER!", True, color.black)
        msg1_width = msg1.get_width()
        msg1_height = msg1.get_height()
        win.blit(msg1, (width// 2 - msg1_width // 2, height // 2 - msg1_height // 2))
        done = True
    #player lost
    if ball_x<0:
        msg2 = font.render("LOSER", True, color.red)
        msg2_width = msg2.get_width()
        msg2_height = msg2.get_height()
        win.blit(msg2, (width // 2 - msg2_width // 2, height// 2 - msg2_height // 2))
        done = True
    if paddle_x <=ball_x <= paddle_x + paddle_width and paddle_y<=ball_y+ball_height/2<=paddle_y+paddle_height:
        #increase ball speed
        dx*=1.2
        dy*=1.2
        # change score counter on the screen
        score+=1
        # change score counter on the screen
        msg = font.render("Score: " + str(score), True, color.black)
        done=False
    # check for any new events in the event queue
    for event in pygame.event.get():
        # event will be a single event object
        if event.type == pygame.QUIT:
            # exit the program
            # use the built-in exit() function to quit
            exit()
        elif event.type == pygame.KEYDOWN:
            # the user has pressed a key
            # what key did they press?
            if event.key == pygame.K_DOWN:
                # the user pressed the down key
                paddle_y += paddle_dy
            elif event.key == pygame.K_UP:
                # the user pressed the up key
                paddle_y -= paddle_dy
        elif event.type == pygame.MOUSEMOTION:
            # get the position of the mouse
            mouse_x, mouse_y = event.pos
            # move the paddle down the screen 5 pixels at a time
            if mouse_y > paddle_y:
                paddle_y += paddle_dy
            # move the paddle up the screen 5 pixels at a time
            elif mouse_y < paddle_y:
                paddle_y -= paddle_dy

    # get the elapsed time
    # limit the maximum frame rate to 60fps to keep our animation
    # from going "too fast"
    # convert from ms -> s
    dt = clock.tick(60) / 100
    # move ball
    (ball_x, ball_y, dx, dy) = move(ball_x, ball_y, dx, dy, dt)
    # draw the ball on the window
    win.blit(ball, (ball_x, ball_y))
    #show the score
    win.blit(msg, (width - 2 * msg_width, msg_height // 2))
    # check the paddle is still inside the window
    if paddle_y < 0:
        paddle_y = 0
    elif paddle_y + paddle_height >= height:
        paddle_y = height - paddle_height

    # draw the paddle
    win.blit(paddle, (paddle_x, paddle_y))

    # update window
    pygame.display.update()

pygame_helper.wait_for_click()
# show score
if score < 10:
    # user lost
    print("GAME OVER. You scored", score, "points.")
else:
    # user won
    print("Congratulations! You won with a score of", score, "points!")

#Welcome to pong!
#The rules:
#You will be rewarded a point each time ball touches the paddle.
#Ball will increase in velocity each time the ball hits the paddle.
#Try to not let the ball hit the left side of the wall, if you do, you lose.
#Waiting for click
#Waiting for click
#GAME OVER. You scored 2 points.