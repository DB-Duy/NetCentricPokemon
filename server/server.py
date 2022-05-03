import socket
import _thread
import pickle

server = "192.168.100.2"
port = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Players = {}

try:
  sock.bind((server,port))
except socket.error as e:
  print(str(e))
  
sock.listen()
print("Sever listening")

def newClient(conn,addr):
  reply = {}
  try:
    print(f"Sending ID: {addr}")
    conn.sendall(str(addr).encode('utf-8'))
  except:
    return
  while True:
    try: 
      data = conn.recv(2048*4)
      clientPos = pickle.loads(data)
      ((id, pos),) = clientPos.items()
      Players[id]=pos
      reply ={k:v for (k,v) in Players.items() if k!=id}
      conn.sendall(pickle.dumps(reply))
    except:
      break
  conn.close()
  
while True:
  conn, addr = sock.accept()
  print(f"Client connected: {addr}")
  _thread.start_new_thread(newClient, (conn, addr))
