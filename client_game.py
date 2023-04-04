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

def winning(win, score, colour):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont("impact", 60)
    score_str = f"{score[0]} : {score[1]} "
    score = font.render(score_str, True, colour)
    inst = font.render("Press Enter to continue..", True, (0, 255, 0))
    text = font.render("You Win :)", True, colour)
    pos_x1 = (screen_width - text.get_width())// 2
    pos_y1 = (screen_height- text.get_height())// 2

    pos_x2 = (screen_width - score.get_width())// 2
    pos_y2 = (screen_height - 3*score.get_height())// 2

    pos_x3 = (screen_width - inst.get_width())// 2
    pos_y3 = (screen_height + 3*inst.get_height())// 2

    win.blit(text, (pos_x1, pos_y1))
    win.blit(score, (pos_x2, pos_y2))
    win.blit(inst, (pos_x3, pos_y3))

    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run = False

    menu_screen()

def losing(win, score, colour):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont("impact", 60)
    score_str = f"{score[0]} : {score[1]} "
    score = font.render(score_str, True, colour)
    inst = font.render("Press Enter to continue..", True, (0, 255, 0))
    text = font.render("You Lose :(", True, colour)

    pos_x1 = (screen_width - text.get_width())// 2
    pos_y1 = (screen_height- text.get_height())// 2

    pos_x2 = (screen_width - score.get_width())// 2
    pos_y2 = (screen_height - 3*score.get_height())// 2

    pos_x3 = (screen_width - inst.get_width())// 2
    pos_y3 = (screen_height + 3*inst.get_height())// 2

    win.blit(text, (pos_x1, pos_y1))
    win.blit(score, (pos_x2, pos_y2))
    win.blit(inst, (pos_x3, pos_y3))

    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run = False

    menu_screen()


def main():
    global run
    global wins
    wins = [0, 0]
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    game = n.getG()
    p = game.players[player]

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        try:
            game.players[player] = p
            game = n.send(game.players[player])

            if not game:
                # print("here")
                run = False
                break

            if game.connected():
                if game.complete:
                    end_game(game, player)
                    run = False

                else:
                    p = game.players[player]
                    p2 = game.players[not player]
                    tar = game.tarX, game.tarY
                    wins = game.wins
                    redrawWindow(win, p, p2, tar)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.quit()

                    p.move()
                    redrawWindow(win, p, p2, tar)

            else:
                waitWindow(win)

        except Exception as e:
            print(e)
            run = False
            break

def end_game(game, p):
    print("END GAME")
    print(game.wins)
    if game.wins[p] > game.wins[not p]:
        winning(win, game.wins, game.players[p].colour)

    else:
        losing(win, game.wins, game.players[p].colour)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        # font = pygame.font.SysFont("impact", 50)
        text = font.render("Click to Connect!", True, (255,0,255))
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