import socket
import random
import pickle

from window_config import *
from _thread import start_new_thread
from player import Player

server = server_address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( (server, port) )

s.listen()
print("Server Running.")
print("Waiting for a connection...")

width = 40
height = 60
vel = 1
ini_pos = [(width + vel, height + vel), (width + vel, height + 3*vel)]

players = [ Player(0, 0, vel, width, height, (255, 0, 255)), Player(0, 0, vel, width, height, (255, 255, 0))]

def rand_rect(width,height, vel):
    x = random.randint(width + vel, screen_width - width - vel)
    y = random.randint(height + vel, screen_height - height - vel)
    return x , y

def threaded_client(conn, player):
    global target
    global currentPlayer

    # busy wait
    while currentPlayer < 2:
        pass

    players[player].x, players[player].y = ini_pos[player][0], ini_pos[player][1]
    conn.send(pickle.dumps( (players[player], target) ))

    while True:
        try:
            data = pickle.loads( conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                reply = players[0] if player == 1 else players[1]
            if (players[player].x, players[player].y) == target:
                reply = "You Win :)"
                conn.sendall(pickle.dumps(reply))
                break

            elif (players[not player].x, players[not player].y) == target:
                reply = "You Lose :("
                conn.sendall(pickle.dumps(reply))
                break

            else:
                conn.sendall(pickle.dumps(reply))

        except Exception:
            break

    print("Lost connection with player", currentPlayer)
    conn.close()
    currentPlayer -= 1
    if currentPlayer == 0:
        target = rand_rect(width, height, vel)

global target
target = rand_rect(width, height, vel)

global currentPlayer
currentPlayer = 0

while True:
    conn, addr = s.accept() # accept any incoming connection
    print("Connected to: ", addr)

    # busy wait
    while currentPlayer >= 2:
        pass
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1