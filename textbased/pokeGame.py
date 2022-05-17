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
                packet.setPacketPayload(self.__switchPokemon())
            if userInput == "3":
                packet.setPacketInfo(ACTION_SURRENDER)
        return packet

    def __switchPokemon(self):
        payload = {}

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
        last = ""
        while True:
            time.sleep(0.5)
            self.network.sendPacket(self.__pollingPacket())
            serverPacket = self.network.parseServerPacket()
            packetType = serverPacket.getPacketType()
            info = serverPacket.getPacketInfo()

            if packetType == PACKETTYPE_SERVER_RESPONSE and info != last:
                if info == BATTLESTATE_AWAIT_PLAYERS:
                    print("Waiting for other player")
                elif info == BATTLESTATE_AWAIT_OTHER_PLAYER_ACTION:
                    self.gameState = serverPacket.getPacketPayload()
                    print("Waiting for other player's action")
                elif info == BATTLESTATE_AWAIT_ACTION:
                    self.gameState = serverPacket.getPacketPayload()
                    self.network.sendPacket(self.getActionPacket())
                last = info

    def __pollingPacket(self):
        packet = network.Packet()
        packet.setPacketType(PACKETTYPE_POLLING)
        packet.setPacketInfo(f"{self.network.id}")
        return packet
