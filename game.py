import pygame
import random

pygame.init()
screen_width = 1000
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Box")

clientNumber = 0

def rand_rect(width,height, vel):
    x = random.randint(width, screen_width - width)
    y = random.randint(height, screen_height - height)
    return x - x%vel, y - y%vel

def run_game():
    run = True
    x = 50
    y = 50
    vel = 10
    width = 40
    height = 60
    x_tar, y_tar = rand_rect(width, height, vel)
    pygame.draw.rect(win, (0,255,0), (x_tar, y_tar, width, height))
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if x - vel < 0:
                x = screen_width
            x -= vel

        if keys[pygame.K_RIGHT]:
            if x + vel > screen_width:
                x = 0
            x += vel

        if keys[pygame.K_UP]:
            if y - vel < 0:
                y = screen_height
            y -= vel

        if keys[pygame.K_DOWN]:
            if y + vel > screen_height:
                y = 0
            y += vel

        win.fill((0,0,0))
        pygame.draw.rect(win, (0,255,0), (x_tar, y_tar, width, height))
        pygame.draw.rect(win, (255,0,0), (x, y, width, height))
        pygame.display.update()

        if (x, y) == (x_tar, y_tar):
            pygame.time.delay(500)
            win.fill((0,0,0))
            font = pygame.font.SysFont("impact", 50)
            white = (255, 0 ,255)
            txtsurf = font.render("GAME COMPLETE :)", True, white)
            pos_x = (screen_width- txtsurf.get_width())// 2
            pos_y = (screen_height- txtsurf.get_height())// 2
            win.blit(txtsurf,(pos_x, pos_y))
            pygame.display.update()
            pygame.time.delay(2000)
            break

run_game()
pygame.quit()