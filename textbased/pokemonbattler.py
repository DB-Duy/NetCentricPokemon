from CONSTANTS import *
import pokemon


class Battler:
    def __init__(self, teamOne: pokemon.PokeTeam, teamTwo: pokemon.PokeTeam):
        self.teamOne = {pkm.name:pkm.hp for pkm in teamOne.pokemonList}
        self.teamTwo = {pkm.name:pkm.hp for pkm in teamTwo.pokemonList}
        self.teamOneCurrent = None
        self.teamTwoCurrent = None
        
    def setTeamOneCurrent(self, pokemonID):
      self.teamOneCurrent = pokemonID
      
    def setTeamTwoCurrent(self, pokemonID):
      self.teamTwoCurrent = pokemonID
  
    def startBattle(self):
        print("Battle start!!")
        self.isBattling = True

        while(self.isBattling):
            self.playRound()

    def setState(self, state):
        self.state = state

    def execute(self, P1Action, P2Action):
      print("-"*20)
      print(f"Player 1: {P1Action}")
      print(f"Player 2: {P2Action}")
      print("-"*20)
      
    def getCurrentBattleInfo(self):
      info = {}
      info.update(self.teamOne)
      info.update(self.teamTwo)
      info.update({"teamOneCurrent":self.teamOneCurrent})
      info.update({"teamTwoCurrent":self.teamTwoCurrent})
      return info