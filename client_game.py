import pygame
from network import Network
from window_config import *

pygame.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FUSE")

def redrawWindow(win, player, player2, target):
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (0, 255, 0), (target[0], target[1], player.width, player.height))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    p = n.getP()
    tar = n.getTar()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        obj = n.send(p)

        if type(obj) == str:
            end_game(obj, p)
            run = False
            break
        else:
            p2 = obj

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2, tar)

def end_game(obj, p):
    pygame.time.delay(800)
    win.fill((0,0,0))
    font = pygame.font.SysFont("impact", 50)
    colour = p.colour
    txtsurf = font.render("GAME COMPLETE.", True, (255, 255, 255))
    pos_x = (screen_width- txtsurf.get_width())// 2
    pos_y = (screen_height- txtsurf.get_height())// 2
    win.blit(txtsurf,(pos_x, pos_y))

    txtsurf1 = font.render(obj, True, colour)
    pos_x1 = (screen_width - txtsurf1.get_width())// 2
    pos_y1 = (screen_height- 3*txtsurf1.get_height())// 2
    win.blit(txtsurf1,(pos_x1, pos_y1))

    pygame.display.update()
    pygame.time.delay(2000)

main()
