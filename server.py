import socket
import pickle

from window_config import *
from _thread import start_new_thread
from game import Game

server = server_address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( (server, port) )

global idCount
global games
global ack
games = {}
ack = {}
connected = set()

# no. of clients connected
idCount = 0

s.listen()
print("Server Running.")
print("Waiting for a connection...")

def threaded_client(conn, player, gameID):
    global games
    global ack
    conn.send(pickle.dumps((player, games[gameID])))
    run = True
    while run:
        try:
            data = pickle.loads( conn.recv(4096) )

            if not data:
                print("Disconnected")
                break

            if gameID not in games.keys():
                print("Disconnected")
                break

            if gameID in games.keys():
                game = games[gameID]

                if not game.connected():
                    conn.sendall(pickle.dumps(game))
                    continue


                elif game.complete:
                    if ack[gameID] == [True, True]:
                        run = False
                        break

                    if not ack[gameID][player]:
                        conn.sendall(pickle.dumps(game))
                        ack[gameID][player] == True

                else:
                    game.players[player] = data

                    if game.hasHitTar(player):
                        game.addWin(player)

                        if not game.complete:
                            game.getNewTar()


                    if game.complete:
                        ack[gameID][player] = True

                    games[gameID] = game
                    conn.sendall(pickle.dumps(game))

        except Exception as e:
            break

    print("Lost Connection")

    try:
        del games[gameID]
        del ack[gameID]
        print("Closing Game", gameID)

    except Exception:
        pass

    global idCount
    idCount -= 1
    conn.close()

while True:
    # accept any incoming connection
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameID = (idCount - 1)// 2

    # new game created
    if idCount % 2 == 1:
        games[gameID] = Game(gameID)

    else:
        games[gameID].ready = True
        ack[gameID] = [False, False]
        p = 1

    print(p, gameID)
    start_new_thread(threaded_client, (conn, p, gameID))