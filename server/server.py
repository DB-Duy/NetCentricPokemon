import socket
import _thread
import pickle
import time

from ThreadClientPokeCat import *
# setup sockets
server = socket.gethostbyname(socket.gethostname())
port = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set constants

#Dynamic variables
Players = {}
Pokemons = {}
connections = 0

# start server 
try:
  sock.bind((server,port))
except socket.error as e:
  print("[SERVER] Binding error: ",str(e))
  quit()
  
sock.listen()
print(f"[SERVER] Server listening with local ip {server} port {port} ")

# MAIN LOOP   
while True:
  time.sleep(0.5)
  conn, addr = sock.accept()
  print(f"[CONNECTION] Client connected: {addr}")
  _thread.start_new_thread(thread_client_pokecatch, (Players,Pokemons,conn, addr))
  connections +=1

## End game