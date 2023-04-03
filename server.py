import socket
import random
import pickle

from window_config import *
from _thread import start_new_thread
from player import Player
from game import Game

server = server_address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( (server, port) )

# games dictionary:
games = {}
connected = set()

# no. of clients connected
idCount = 0

s.listen()
print("Server Running.")
print("Waiting for a connection...")

def threaded_client(conn, player, gameID):
    global idCount
    # conn.send(pickle.dumps(games[gameID].players[player]))
    conn.send(pickle.dumps((player, games[gameID])))
    run = True
    while run:
        try:
            data = pickle.loads( conn.recv(4096) )

            if gameID in games:
                game = games[gameID]

                if not data:
                    print("Disconnected")
                    break

                elif not game.connected():
                    conn.sendall(pickle.dumps(game))
                    continue

                else:
                    game.players[player] = data

                    if game.hasHitTar(player):
                        game.addWin(player)

                        if game.complete:
                            run = False
                        else:
                            game.getNewTar()

                    games[gameID] = game
                    conn.sendall(pickle.dumps(game))

        except Exception as e:
            print("here", e)
            break

    print("Lost Connection")

    try:
        del games[gameID]
        print("Closing Game", gameID)

    except Exception:
        pass

    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept() # accept any incoming connection
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameID = (idCount - 1)// 2

    # new game created
    if idCount % 2 == 1:
        games[gameID] = Game(gameID)

    else:
        games[gameID].ready = True
        p = 1

    print(p, gameID)
    start_new_thread(threaded_client, (conn, p, gameID))