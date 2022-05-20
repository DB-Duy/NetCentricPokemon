import socket
import _thread
import pokemonbattler
import json
import time
import player
import pokemon
from network import Packet

from CONSTANTS import *


class Server:
    def __init__(self, serverIP):
        self.server = serverIP
        self.port = 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.battleHandler = BattleHandler()

        try:
            self.sock.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))

    def start(self):
        self.sock.listen()
        print("Server listening at "+self.server+":"+str(self.port))
        while True:
            conn, addr = self.sock.accept()
            print(f"Client connected: {addr}")
            _thread.start_new_thread(self.newClient, (conn, addr))

    def newClient(self, conn, addr):
        try:
            conn.sendall(str(addr).encode('utf-8'))
            self.clients[str(addr)] = conn
        except:
            return
        while True:
            try:
                data = conn.recv(2048*64).decode('utf-8')
                time.sleep(0.5)
                if data:
                  data = json.loads(data)
                  packet = Packet(data)
                  self.battleHandler.handlePacket(packet, addr)
                  reply = self.battleHandler.getPacket(addr)
                  reply = json.dumps(reply.getPacketDict())
                  print("P1: "+(self.battleHandler.playerOneAction if self.battleHandler.playerOneAction else "None"))
                  print("P2: "+(self.battleHandler.playerTwoAction if self.battleHandler.playerTwoAction else "None"))
                  conn.sendall(reply.encode())
                else:
                  raise socket.error

            except socket.error:
                del self.clients[str(addr)]
                self.battleHandler.removePlayer(addr)
                self.battleHandler.clearActions()
                break
        conn.close()


class BattleHandler:
    def __init__(self):
        self.state = BATTLESTATE_AWAIT_PLAYERS
        self.battler = None
        
        self.playerOne = None
        self.playerOneAddr = ""
        self.playerOneStarter = ""
        
        self.playerTwo = None
        self.playerTwoAddr = ""
        self.playerTwoStarter = ""
        
        self.playerNum = 0
        
        self.playerOneAction = None
        self.playerTwoAction = None
        
    def addPlayer(self, packet: Packet, addr):
        info = packet.getPacketInfo()
        if self.playerOneAddr == "":
            team = pokemon.PokeTeam()
            for pkm in info['pokemon']:
                p = pokemon.Pokemon(info['pokemon'][pkm])
                team.addPokemon(p)
            self.playerOne = player.Player(info['name'], team)
            self.playerOneAddr = addr
            self.playerOneStarter = info['starting']
            print("Added player 1")
            self.playerNum += 1
        elif self.playerTwoAddr == "":
            team = pokemon.PokeTeam()
            for pkm in info['pokemon']:
                p = pokemon.Pokemon(info['pokemon'][pkm])
                team.addPokemon(p)
            self.playerTwo = player.Player(info['name'], team)
            self.playerTwoAddr = addr
            self.playerTwoStarter = info['starting']
            print("Added player 2")
            self.playerNum += 1
        else:
            print("BATTLE ALREADY HAS 2 PLAYERS")

    def removePlayer(self, addr):
        if addr == self.playerOneAddr:
            print("Removed player 1")
            self.playerOne = None
            self.playerOneAddr = ""
            self.playerOneStarter = ""
            self.playerNum -= 1
        if addr == self.playerTwoAddr:
            print("Removed player 2")
            self.playerTwo = None
            self.playerTwoAddr = ""
            self.playerTwoStarter = ""
            self.playerNum -= 1
        if self.playerNum<2:
          self.battler = None
        
    def handlePacket(self, packet: Packet, addr):
        if packet.getPacketType() == PACKETTYPE_HANDSHAKE:
            return self.addPlayer(packet, addr)
        elif packet.getPacketType() == PACKETTYPE_PLAYER_ACTION:
            return self.handlePlayerAction(packet, addr)
          

    def handlePlayerAction(self, packet: Packet, addr):      
      if addr == self.playerOneAddr:
        if packet.getPacketInfo() == ACTION_SWITCH:
          self.playerOneAction = ACTION_SWITCH + "---" + packet.getPacketPayload()
        else:
          self.playerOneAction = packet.getPacketInfo()
      elif addr == self.playerTwoAddr:
        if packet.getPacketInfo() == ACTION_SWITCH:
          self.playerTwoAction = ACTION_SWITCH + "---" + packet.getPacketPayload()
        else:
          self.playerTwoAction = packet.getPacketInfo()
      if self.playerOneAction and self.playerTwoAction:
        self.executeAction(self.playerOneAction, self.playerTwoAction)
        self.updateState()
        
    def clearActions(self):
      self.playerTwoAction = None
      self.playerOneAction = None
        
    def executeAction(self, P1Action, P2Action):
      self.battler.execute(P1Action, P2Action)
      self.clearActions()
      
    def getPacket(self, addr):
      self.updateState()
      if self.state == BATTLESTATE_AWAIT_PLAYERS:
        return self.awaitPlayersPacket()
      elif self.state == BATTLESTATE_AWAIT_ACTION:
        if addr == self.playerOneAddr and self.playerOneAction is None:
          return self.awaitActionPacket()
        elif addr == self.playerTwoAddr and self.playerTwoAction is None:
          return self.awaitActionPacket()
        else:
          return self.awaitOtherPacket()
      
    def updateState(self):
      if self.playerOneAddr == "" or self.playerTwoAddr == "":
        self.state = BATTLESTATE_AWAIT_PLAYERS
      elif self.playerOneAction is None or self.playerTwoAction is None:
        if self.battler is None:
          self.battler = pokemonbattler.Battler(self.playerOne.team, self.playerTwo.team)
          self.battler.setTeamOneCurrent(self.playerOneStarter)
          self.battler.setTeamTwoCurrent(self.playerTwoStarter)
        self.state = BATTLESTATE_AWAIT_ACTION

      
    def awaitPlayersPacket(self):
      packet = Packet()
      packet.setPacketType(PACKETTYPE_SERVER_RESPONSE)
      packet.setPacketInfo(BATTLESTATE_AWAIT_PLAYERS)
      return packet
    
    def awaitOtherPacket(self):
      packet = Packet()
      packet.setPacketType(PACKETTYPE_SERVER_RESPONSE)
      packet.setPacketInfo(BATTLESTATE_AWAIT_OTHER_PLAYER_ACTION)
      info = self.battler.getCurrentBattleInfo()
      info['teamOneID'] = self.playerOneAddr
      info['teamTwoID'] = self.playerTwoAddr
      packet.setPacketPayload(info)
      return packet
    
    def awaitActionPacket(self):
      packet = Packet()
      packet.setPacketType(PACKETTYPE_SERVER_RESPONSE)
      packet.setPacketInfo(BATTLESTATE_AWAIT_ACTION)
      info = self.battler.getCurrentBattleInfo()
      info['teamOneID'] = self.playerOneAddr
      info['teamTwoID'] = self.playerTwoAddr
      packet.setPacketPayload(info)
      return packet
    
      

server = Server(SERVER_IP)
server.start()
