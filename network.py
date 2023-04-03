import socket
import pickle
import window_config

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = window_config.server_address
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p, self.game = self.connect()
        # initial_msg = self.connect()
        # self.p = initial_msg[0]
        # self.tar = initial_msg[1]

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except ConnectionRefusedError:
            print("Connection Refused")

    def getP(self):
        return self.p

    def getG(self):
        return self.game

    def getTar(self):
        return self.tar

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))

        except socket.error as e:
            print(e)