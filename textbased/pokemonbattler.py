from CONSTANTS import *
import pokemon


class Battler:
    def __init__(self, teamOne: pokemon.PokeTeam, teamTwo: pokemon.PokeTeam):
        self.__teamOne = teamOne
        self.__teamTwo = teamTwo
        self.teamOne = [[pkm.ID,pkm.name,pkm.hp] for pkm in teamOne.pokemonList]
        self.teamTwo = [[pkm.ID,pkm.name,pkm.hp] for pkm in teamTwo.pokemonList]
        self.teamOneCurrent = None
        self.teamTwoCurrent = None
        
    def setTeamOneCurrent(self, pokemonID):
      self.teamOneCurrent = self.__teamOne.getPokemonFromID(pokemonID)
      
    def setTeamTwoCurrent(self, pokemonID):
      self.teamTwoCurrent = self.__teamTwo.getPokemonFromID(pokemonID)
      
    def execute(self, P1Action, P2Action):
      print("-"*20)
      print(f"Player 1: {P1Action}")
      print(f"Player 2: {P2Action}")
      print("-"*20)
      
    def getCurrentBattleInfo(self):
      info = {}
      info.update({"teamOne":self.teamOne})
      info.update({"teamTwo":self.teamTwo})
      info.update({"teamOneCurrent":self.teamOneCurrent.ID})
      info.update({"teamTwoCurrent":self.teamTwoCurrent.ID})
      return info