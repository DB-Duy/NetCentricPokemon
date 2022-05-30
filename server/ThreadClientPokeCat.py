from asyncio.windows_events import NULL
import pickle
import time

from PokeCatchHelper import catch_pokemon
posMsg =""
replyMsg =""
conn_id = NULL
def thread_client_pokecatch(Players,Pokemons,Pokemons_packet, conn,addr):
  """ start a new thread for new client connected to pokecatch's server

  Args:
      Players (set): All available clients
      Pokemons (set): All available pokemons
      conn (socket object): current client socket
      addr (address info): current client address info
  """
  global conn_id 
  conn_id = addr
  reply = {}
  ## Remove posMsg and replyMsg for better perfromance 
  global posMsg,replyMsg
  try:
    print(f"Sending ID: {addr}")
    conn.sendall(str(addr).encode('utf-8'))
  except:
    return
  while True:
    try: 
      data = conn.recv(2048*4)
      if not data:
        break
      clientData = pickle.loads(data)
      posPrintOut =f"[CLIENT {conn_id}] Position: {clientData}"
      if posMsg != posPrintOut:
        print(posPrintOut)
        posMsg = posPrintOut
      ((id, pos),) = clientData.items()
      Players[id]=pos
      
      if pos[3].split(" ")[0] == 'CATCH':
        pokemon = catch_pokemon(Pokemons,Pokemons_packet,int(pos[3].split(" ")[1]))
        conn.sendall(pickle.dumps(pokemon))
        continue
      reply ={k:v for (k,v) in Players.items() if k!=id}
      replyPrintOut = f"[CLIENT {conn_id}] Reply: {reply}"
      
      if replyMsg != replyPrintOut:
        print(replyPrintOut)
        replyMsg = replyPrintOut
      conn.sendall(pickle.dumps(reply))
      conn.sendall(pickle.dumps(Pokemons_packet))
    except Exception as e:
      print(e)
      break
    time.sleep(0.001)
  conn.close()
  
## When user disconnects
  print(f"[DISCONNECT] Client {conn_id} is disconnected")
  del Players[str(conn_id)]