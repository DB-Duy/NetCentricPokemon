import player
import pokemon
import network
import time
import json
from CONSTANTS import *


class Game:
    def __init__(self):
        self.player = None
        self.__setPlayer()
        self.network = None
        self.startingPokemonID = None

        self.gameState = {}
        self.teamNum = None

    def __setPlayer(self):
        print("1.Load player or 2.create new player ?")
        validInputs = ["1", "2"]
        userInput = input()
        while userInput not in validInputs:
            userInput = input("Invalid input")
        if userInput == "1":
            self.__loadPlayer()
        if userInput == "2":
            self.__createPlayer()

    def __loadPlayer(self):
        self.player = player.Player.loadPlayer()

    def __createPlayer(self):
        userInput = input("Input your character name: ")
        self.player = player.Player(userInput, pokemon.PokeTeam())

    def joinServer(self, serverIP):
        if self.player.validToJoinGame():
            if self.__promptBattle() and self.__pickStartingPokemon():
                self.network = network.Network(serverIP)
                self.__sendHandshake()
                self.__startGameLoop()

    def __pickStartingPokemon(self):
        validInputs = ["1", "2", "3"]
        userInput = ""
        while userInput not in validInputs:
            print("Please pick starting pokemon:")
            for idx, name in enumerate(self.player.team.getBattlePokemonNames()):
                print(f"{idx+1}. {name}   ", end="")
            userInput = input("\n")
        self.startingPokemonID = self.player.team.battleList[int(userInput)-1]
        return True

    def __promptBattle(self):
        validInputs = ["1", "2"]
        userInput = ""
        while userInput not in validInputs:
            print(
                "What would you like to do: 1.Accept battle 2.Decline battle")
            userInput = input()
            if userInput == "2":
                print("Battle declined")
                return False
            if userInput == "1":
                print("Battle accepted")
                return True
            else:
                print("Invalid input")

    def getActionPacket(self):
        if self.hasToSwitch():
            return self.__forcedSwitchPaket()
        validInputs = ["1", "2", "3"]
        packet = network.Packet()
        packet.setPacketType(PACKETTYPE_PLAYER_ACTION)
        userInput = ""
        while userInput not in validInputs:
            print("What would you like to do: 1.Attack 2.Deploy 3.Surrender")
            userInput = input()
            if userInput == "1":
                packet.setPacketInfo(ACTION_ATTACK)
            if userInput == "2":
                packet.setPacketInfo(ACTION_SWITCH)
                payload = self.__switchPokemon()
                if payload:
                    packet.setPacketPayload(payload)
                else:
                    userInput = ""
                    continue
                
            if userInput == "3":
                packet.setPacketInfo(ACTION_SURRENDER)
        return packet
    
    def hasToSwitch(self):
        team = None
        current = None
        if self.teamNum == 'teamOne':
            team = self.gameState['teamOne']
            current = self.gameState['teamOneCurrent']
        else:
            team = self.gameState['teamTwo']
            current = self.gameState['teamTwoCurrent']
        
        for [ID,_,HP] in team:
            if ID == current and HP <= 0:
                return True
        return False

    def __forcedSwitchPaket(self):
        packet = network.Packet()
        packet.setPacketType(PACKETTYPE_PLAYER_ACTION)
        packet.setPacketInfo(ACTION_SWITCH)
        payload = None
        while payload is None:
            payload = self.__switchPokemon()
        packet.setPacketPayload(payload)
        return packet

    def __switchPokemon(self):        
        team = None
        current = None
        print(f"Team num: {self.teamNum}")
        if self.teamNum == 'teamOne':
            team = self.gameState['teamOne']
            current = self.gameState['teamOneCurrent']
        else:
            team = self.gameState['teamTwo']
            current = self.gameState['teamTwoCurrent']
            
        validInputs = [str(idx+1) for idx,[ID,_,pkmHP] in enumerate(team) if pkmHP>0 and ID != current]
        validInputs.append(str(int(validInputs[-1])+1))
        userInput = ""
        while userInput not in validInputs:
            print("Pick pokemon to switch:")
            for idx,[ID,pkmName, pkmHP] in enumerate(team):
                    if pkmHP<=0:
                        print(f"{idx+1}.{pkmName} - LOST",end="  ")
                    elif ID == current:
                        print(f"{idx+1}.{pkmName} - {pkmHP} HP - CURRENTLY BATTLING",end=" ")
                    else:
                        print(f"{idx+1}.{pkmName} - {pkmHP} HP - READY TO BATTLE",end=" ")
            print(f"{validInputs[-1]}. Cancel switch")
            userInput = input()
        if userInput == validInputs[-1]:
            return None
        else:
            return team[int(userInput)-1][0]

    def __sendHandshake(self):
        packet = network.Packet()
        packet.setPacketType(PACKETTYPE_HANDSHAKE)
        data = {}
        for pkmID in self.player.team.battleList:
            pkm = self.player.team.getPokemonFromID(pkmID)
            data.update({pkm.name: pkm.getPokemonInfo()})
        handshake = {"pokemon": data, "name": self.player.name,
                     "starting": self.startingPokemonID}
        packet.setPacketInfo(handshake)

        self.network.sendPacket(packet)

    def __startGameLoop(self):
        while True:
            time.sleep(0.5)
            packet = None
            serverPacket = self.network.parseServerPacket()
            packetType = serverPacket.getPacketType()
            info = serverPacket.getPacketInfo()
            
            if packetType == PACKETTYPE_SERVER_RESPONSE:
                if info == BATTLESTATE_P1_VICTORY or info == BATTLESTATE_P2_VICTORY:
                    self.endGame(serverPacket)
                    break
                elif info == BATTLESTATE_AWAIT_ACTION:
                    self.setGameState(serverPacket.getPacketPayload())
                    packet = self.getActionPacket()
                elif info == BATTLESTATE_AWAIT_OTHER_PLAYER_ACTION:
                    self.setGameState(serverPacket.getPacketPayload())
                    print("Waiting for other player's action")
                elif info == BATTLESTATE_AWAIT_PLAYERS:
                    print("Waiting for other player")
            
            if packet is None:
                packet = self.__pollingPacket()
            if self.teamNum is None:
                self.__setTeamNum()
            self.network.sendPacket(packet)
            
    def endGame(self,resultPacket: network.Packet):
        result = resultPacket.getPacketPayload()
        if result['winner'] == self.teamNum:
            print("YOU WIN")
            for pkmID in self.player.team.battleList:
                self.player.team.getPokemonFromID(pkmID).giveExp(result['expRewards'])
            self.player.savePlayer()
        else:
            print("YOU LOST")
            
    def setGameState(self,state):
        self.gameState = state
        if self.teamNum is None:
            self.__setTeamNum()
    
    def __setTeamNum(self):
        if self.gameState:
            if self.network.id == str(tuple(self.gameState['teamOneID'])):
                self.teamNum = 'teamOne'
            elif self.network.id == str(tuple(self.gameState['teamTwoID'])):
                self.teamNum = 'teamTwo'

    def __pollingPacket(self):
        packet = network.Packet()
        packet.setPacketType(PACKETTYPE_POLLING)
        packet.setPacketInfo(f"{self.network.id}")
        return packet
