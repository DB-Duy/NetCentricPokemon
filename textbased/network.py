import socket
import json
import struct

from CONSTANTS import *

class Packet:
  def __init__(self, packetBody={}):
    self.packetBody = packetBody
    
  def setPacketType(self, type):
    self.packetBody['type']=type
  
  def getPacketType(self):
    return self.packetBody['type']
    
  def setPacketInfo(self, info):
    self.packetBody['info']=info
    
  def setPacketPayload(self, payload: dict):
    self.packetBody['payload'] = payload
    
  def getPacketPayload(self):
    return self.packetBody['payload']
  
  def getPacketInfo(self):
    return self.packetBody['info']
    
  def getPacketDict(self):
    return self.packetBody

class Network:
    def __init__(self, serverIP):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverIP
        self.port = 9999
        self.addr = (self.server, self.port)
        self.id=list(self.connect())
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def sendPacket(self, packet: Packet) -> Packet:
        try:
            data = json.dumps(packet.getPacketDict())
            data = data.encode()
            self.client.sendall(data)
        except socket.error as e:
            print(e)

    def parseServerPacket(self):
      serverRes = self.client.recv(2048*64)
      data = serverRes.decode()
      print(data)
      data = json.loads(serverRes)
      return Packet(data)
