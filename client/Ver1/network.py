import socket
import pickle
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.168.1"  ## Get local IP address
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id=self.connect()
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def sendPlayerState(self, player):
        data = pickle.dumps({player.id:(player.x,player.y)})
        try:
            self.client.sendall(data)
            return self.client.recv(2048)
        except socket.error as e:
            print(e)
