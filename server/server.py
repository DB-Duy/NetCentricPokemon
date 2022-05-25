import socket
import _thread
import pickle
import time

server = socket.gethostbyname(socket.gethostname())
port = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Players = {}

try:
  sock.bind((server,port))
except socket.error as e:
  print("Binding error ",str(e))
  
sock.listen()
print("Server listening")

def newClient(conn,addr):
  reply = {}
  try:
    print(f"Sending ID: {addr}")
    conn.sendall(str(addr).encode('utf-8'))
  except:
    return
  while True:
    time.sleep(0.5)
    try: 
      data = conn.recv(2048*4)
      print("Client data",data)
      clientPos = pickle.loads(data)
      ((id, pos),) = clientPos.items()
      Players[id]=pos
      reply ={k:v for (k,v) in Players.items() if k!=id}
      print("Reply: ",reply)
      conn.sendall(pickle.dumps(reply))
    except:
      break
  conn.close()
  
while True:
  conn, addr = sock.accept()
  print(f"Client connected: {addr}")
  _thread.start_new_thread(newClient, (conn, addr))
