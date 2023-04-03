import pygame
from network import Network
from window_config import *

pygame.font.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FUSE")

def redrawWindow(win, player, player2, target):
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (0, 255, 0), (target[0], target[1], player.width, player.height))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def waitWindow(win):
    win.fill((128, 128, 128))
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Waiting for another player..", True, (255,0,255))
    pos_x1 = (screen_width - text.get_width())// 2
    pos_y1 = (screen_height- text.get_height())// 2
    win.blit(text, (pos_x1, pos_y1))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    game = n.getG()
    p = game.players[player]

    while run:
        clock.tick(60)
        game = n.send(game.players[player])

        if not game:
            run = False
            break

        if game.connected():
            if game.complete:
                # end_game(game, p)
                run = False
                break

            else:
                p = game.players[player]
                p2 = game.players[not player]
                tar = game.tarX, game.tarY
                redrawWindow(win, p, p2, tar)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                p.move()
                game.players[player] = p
                redrawWindow(win, p, p2, tar)

        else:
            waitWindow(win)

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

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        # font = pygame.font.SysFont("impact", 50)
        text = font.render("Click to Play!", True, (255,0,255))
        pos_x1 = (screen_width - text.get_width())// 2
        pos_y1 = (screen_height- text.get_height())// 2
        win.blit(text, (pos_x1, pos_y1))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()