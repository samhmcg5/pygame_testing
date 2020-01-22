import sys
import pygame

pygame.init()

size = width, height = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)

gameDisplay = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode(size)

ball_img = pygame.image.load("circle.png")
ball_size = 7

clock = pygame.time.Clock()

def ball(x,y):
    gameDisplay.blit(ball_img, (x,y))

def draw_ball(x,y):
    pygame.draw.circle(gameDisplay, white, (x,y), 10)

def game_loop():
    x = int(width * 0.45)
    y = int(height * 0.8)

    x_change = 0
    y_change = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ############################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
            ######################

        if (x > width - ball_size and x_change > 0) or (x < 0 and x_change < 0):
            x_change = 0
        if (y > height - ball_size and y_change > 0) or (y < 0 and y_change < 0):
            y_change = 0

        x += x_change
        y += y_change
        gameDisplay.fill(black)
        draw_ball(x,y)

        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()



