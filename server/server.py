
import socket
import _thread
import pickle
import time
import sys
import os
from PokeCatchHelper import *

from APIRequest import PokemonGetter
from ThreadClientPokeCat import thread_client_pokecatch


# setup sockets
server = socket.gethostbyname(socket.gethostname())
port = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set constants

#Dynamic variables
Players = {}
Pokemons = {}
Pokemons_packet = {"isPokemonPacket": True}
connections = 0

# start server 
try:
  sock.bind((server,port))
except socket.error as e:
  print("[SERVER] Binding error: ",str(e))
  quit()
  
sock.listen()
print(f"[SERVER] Server listening with local ip {server} port {port} ")

_thread.start_new_thread(thread_spawn_wave, (Pokemons,Pokemons_packet,Players))
# # MAIN LOOP   
while True:
  conn, addr = sock.accept()
  print(f"[CONNECTION] Client connected: {addr}")
  _thread.start_new_thread(thread_client_pokecatch, (Players,Pokemons,Pokemons_packet,conn, addr))


# ## End game