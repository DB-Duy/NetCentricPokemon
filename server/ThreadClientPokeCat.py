import pickle
import time
def thread_client_pokecatch(Players,Pokemons, conn,addr):
  """ start a new thread for new client connected to pokecatch's server

  Args:
      Players (set): All available clients
      Pokemons (set): All available pokemons
      conn (socket object): current client socket
      addr (address info): current client address info
  """
  conn_id = addr[1]
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
      print(f"[CLIENT {conn_id}] Position: {clientPos}")
      ((id, pos),) = clientPos.items()
      Players[id]=pos
      reply ={k:v for (k,v) in Players.items() if k!=id}
      print(f"[CLIENT {conn_id}] Reply: {reply}")
      conn.sendall(pickle.dumps(reply))
    except Exception as e:
      print(e)
      break
    time.sleep(1)
  conn.close()
  
## When user disconnects
  print(f"[DISCONNECT] Client {conn_id} is disconnected")
