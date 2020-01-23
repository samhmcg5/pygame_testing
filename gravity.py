import sys
import pygame
import math
from random import random

from agent import AgentThread
from defines import Action

# Run with an agent?
run_agent = False
if len(sys.argv) > 1 and sys.argv[1] == '-a':
    run_agent = True

pygame.init()

size = width, height = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)
red = (178, 34, 34)
delta_t = (1.0/60.0)
gravity = 200

gameDisplay = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 12)

def kinematic(vel, acc):
    change = vel*delta_t + 0.5*acc*math.pow(delta_t, 2)
    vel += acc*delta_t
    return change, vel

def showText(x, y, text):
    text = font.render(text, True, white)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    gameDisplay.blit(text, text_rect)

class Goal():
    def __init__(self, x, y, rad, color):
        self.rad = rad
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, self.rad, self.rad)

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.rect)

    def reset(self):
        self.x = int(random() * width)
        self.y = int(random() * height)
        self.rect.center = (self.x,self.y)

    def collides(self, shape):
        if self.rect.colliderect(shape):
            return True
        else:
            return False

    def get_rect(self):
        return self.rect

    def get_pos(self):
        return self.x, self.y

class Ball():
    def __init__(self, x, y, rad, color):
        self.x        = int(x)
        self.y        = int(y)
        self.rad      = rad
        self.color    = color
        self.x_change = 0
        self.y_change = 0
        self.x_vel    = 0
        self.y_vel    = 0
        self.x_acc    = 0
        self.y_acc    = 200
        self.x_dir    = 0
        self.rect = pygame.Rect(self.x, self.y, 2*self.rad, 2*self.rad)

    def draw(self):
        x = int(self.x)
        y = int(self.y)
        self.rect = pygame.draw.circle(gameDisplay, self.color, (x, y), self.rad)

    def get_rect(self):
        return self.rect

    def size(self):
        return self.rad

    def get_pos(self):
        return self.x, self.y

    def get_vel(self):
        return self.x_vel, self.y_vel

    def left(self):
        self.x_vel = -150
        self.x_dir = -1
        self.x_acc = 0
    def right(self):
        self.x_vel = 150
        self.x_dir = 1
        self.x_acc = 0
    def up(self):
        self.y_vel = -150
    def release_x(self, event):
        if (event == "LEFT" and self.x_dir < 0) or (event == "RIGHT" and self.x_dir > 0):
            self.x_acc = 200
            if self.x_vel > 0:
                self.x_acc *= -1

    def update(self):
        self.x_change, self.x_vel = kinematic(self.x_vel, self.x_acc)
        self.y_change, self.y_vel = kinematic(self.y_vel, self.y_acc)
        # Stop if needed
        if (self.x_dir * self.x_vel) < 0:
            self.x_acc = 0
            self.x_vel = 0
            self.x_dir = 0
        # boundaries
        if (self.x > width - self.size() and self.x_change > 0) or \
            (self.x-self.size() < 0 and self.x_change < 0):
            self.x_change = 0
            self.x_vel = -0.5*self.x_vel

        if (self.y > height - self.size() and self.y_change > 0):
            self.y_change = 0
            self.y_vel = -0.5*self.y_vel
            if abs(self.y_vel) < 10:
                self.y_vel = 0
        elif (self.y < 0 and self.y_change < 0):
            self.y_change = 0
            self.y_vel = 0

        # update position
        self.x += self.x_change
        self.y += self.y_change
            

#######################
###     GAME LOOP   ###
#######################
def game_loop(agent=None):
    x = int(width * 0.5)
    y = int(height * 0.8)
    running = True
    # logic states
    collisions = 0
    current_collide = False
    counter = 0

    goal = Goal(0.5*width ,0.1*height, 50, red)
    ball = Ball(x, y, 20, white)

    while running:
        action = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_LEFT:
                    action = Action.LEFT
                elif event.key == pygame.K_RIGHT:
                    action = Action.RIGHT
                elif event.key == pygame.K_UP:
                    action = Action.UP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    action = Action.RELEASE_R if event.key == pygame.K_RIGHT else Action.RELEASE_L
            if event.type == pygame.USEREVENT and agent:
                action = event.key
        
        # Convert key into action
        if action == Action.UP:
            ball.up()
        elif action == Action.LEFT:
            ball.left()
        elif action == Action.RIGHT:
            ball.right()
        elif action == Action.RELEASE_R:
            ball.release_x("RIGHT")
        elif action == Action.RELEASE_L:
            ball.release_x("LEFT")

        ball.update()
        gameDisplay.fill(black)
        goal.draw()
        ball.draw()

        # Am i in the goal?
        current_collide = False
        if goal.collides(ball.get_rect()):
            current_collide = True
            collisions += 1
            showText(0.1*width, 0.1*height, "collision")
            if collisions >= 40:
                collisions = 0
                goal.reset()
        if not current_collide:
            collisions = 0

        # Updates the agents information
        counter += 1
        if agent and counter >= 10:
            ball_x, ball_y = ball.get_pos()
            goal_x, goal_y = goal.get_pos()
            vel_x, vel_y = ball.get_vel()
            agent.tell({"key":"BALL", "x":ball_x, "y":ball_y})
            agent.tell({"key":"GOAL", "x":goal_x, "y":goal_y})
            agent.tell({"key":"VEL", "vel_x":vel_x, "vel_y":vel_y})
            counter = 0

        pygame.display.update()
        clock.tick(60)

# RUN
if __name__ == '__main__':
    if run_agent:
        a = AgentThread()
        a.start()
        game_loop(agent=a)
        a.stop()
    else:
        game_loop()
    
    pygame.quit()
    quit()
