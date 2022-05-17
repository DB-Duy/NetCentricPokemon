import pokemon
import json

from CONSTANTS import *

class Player:
  def __init__(self,playerName: str, team: pokemon.PokeTeam):
    self.name = playerName
    self.team = team
    self.ingame = False
    
  def validToJoinGame(self):
    if len(self.team.getBattlePokemonNames()) != 3:
      print("You need 3 pokemons in your battle list to join battle!")
      return False
    # add other checks here
    return True
  
  def savePlayer(self):
    data = self.team.getPokemonInfos()
    data.update({"name": self.name})
    with open("player.json","w") as f:
      json.dump(data, f)
      
  def loadPlayer():
    data = None
    with open("player.json","r") as f:
      data = json.load(f)
    team = pokemon.PokeTeam()
    team.loadPokemons(data)
    player = Player(data["name"], team)
    return player
    
  def printPlayer(self):
    print(f"Player name: {self.name}")
    print(f"Battle list: ",end="")
    print(self.team.getBattlePokemonNames())
    
  def selectPokemonForBattle(self,pokemonID):
    self.team.selectPokemonForBattle(pokemonID)
