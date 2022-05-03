import socket
import _thread

server = "192.168.100.2"
port = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Players = []

try:
  sock.bind((server,port))
except socket.error as e:
  print(str(e))
  
sock.listen()
print("Sever listening")

def newClient(conn):
  reply = ""
  while True:
    try: 
      data = conn.recv(2048)
      reply = data.decode('utf-8')
      if not data:
        print("Disconnected")
        break
      else:
        print(f"Received: {reply}")
      conn.sendall(str.encode(reply))
    except:
      break
  conn.close()
  
while True:
  conn, addr = sock.accept()
  print(f"Client connected: {addr}")
  _thread.start_new_thread(newClient, (conn,))
