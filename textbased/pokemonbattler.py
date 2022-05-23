from CONSTANTS import *
import pokemon
import random


class Battler:
    def __init__(self, teamOne: pokemon.PokeTeam, teamTwo: pokemon.PokeTeam):
        self.__teamOne = teamOne
        self.__teamTwo = teamTwo
        self.teamOne = [[pkm.ID,pkm.name,pkm.hp] for pkm in teamOne.pokemonList]
        self.teamTwo = [[pkm.ID,pkm.name,pkm.hp] for pkm in teamTwo.pokemonList]
        self.teamOneCurrent = None
        self.teamTwoCurrent = None
        self.teamOneCurrentIdx = None
        self.teamTwoCurrentIdx = None
        
        self.winner = None
        
        self.isBattling = True
        
    def setTeamOneCurrent(self, pokemonID):
      self.teamOneCurrent = self.__teamOne.getPokemonFromID(pokemonID)
      for idx,[ID,_,_] in enumerate(self.teamOne):
        if ID == self.teamOneCurrent.ID:
          self.teamOneCurrentIdx = idx
      print(f"TeamOne switched to {self.__teamOne.getPokemonFromID(pokemonID).name}")
      
    def setTeamTwoCurrent(self, pokemonID):
      self.teamTwoCurrent = self.__teamTwo.getPokemonFromID(pokemonID)
      for idx,[ID,_,_] in enumerate(self.teamTwo):
        if ID == self.teamTwoCurrent.ID:
          self.teamTwoCurrentIdx = idx
      print(f"TeamTwo switched to {self.__teamTwo.getPokemonFromID(pokemonID).name}")
      
    def execute(self, P1Action, P2Action):
      if P1Action == ACTION_ATTACK and P2Action == ACTION_ATTACK:
        self.AttackAttack()
      elif P1Action == ACTION_SURRENDER and P2Action == ACTION_SURRENDER:
        self.SurrenderSurrender()
      elif P1Action == ACTION_SURRENDER:
        self.P1Surrender()
      elif P2Action == ACTION_SURRENDER:
        self.P2Surrender()
      elif ACTION_SWITCH in P1Action and P2Action == ACTION_ATTACK:
        self.SwitchAttack(P1Action.split("---")[1])
      elif P1Action == ACTION_ATTACK and ACTION_SWITCH in P2Action:
        self.AttackSwitch(P2Action.split("---")[1])
      elif ACTION_SWITCH in P1Action and ACTION_SWITCH in P2Action:
        self.SwitchSwitch(P1Action.split("---")[1], P2Action.split("---")[1])
      
      self.resolveRound()
      
      
    def getCurrentBattleInfo(self):
      if self.isBattling:
        info = {}
        info.update({"teamOne":self.teamOne})
        info.update({"teamTwo":self.teamTwo})
        info.update({"teamOneCurrent":self.teamOneCurrent.ID})
        info.update({"teamTwoCurrent":self.teamTwoCurrent.ID})
        return info
      else:
        info = {}
        info.update({"winner": self.winner})
        info.update({"expRewards": self.calculateRewards()})
        return info
    
    def calculateRewards(self):
      rewards = 0
      if self.winner == "teamOne":
        for pkm in self.__teamOne.pokemonList:
          rewards+=pkm.getEXPReward()
      else:
        for pkm in self.__teamTwo.pokemonList:
          rewards+=pkm.getEXPReward()
      return int(rewards/3)
        
    def teamOneAttack(self):
          
      p1Attack = random.choice(["special attack", "physical attack"])
      if p1Attack == "physical attack":
        mult = 1
        damage = self.teamOneCurrent.attack - self.teamTwoCurrent.defense if self.teamOneCurrent.attack > self.teamTwoCurrent.defense else 0
        self.teamTwo[self.teamTwoCurrentIdx][2] -= damage
      else:
        mult = 0
        typeFound = False
        for type in self.teamOneCurrent.type:
          if self.teamTwoCurrent.whenAttacked.get(type):
            typeFound = True
            mult = max(mult, self.teamTwoCurrent.whenAttacked[type])
        if not typeFound:
          mult = 1
        damage = self.teamOneCurrent.specialattack * mult - self.teamTwoCurrent.specialdefense if self.teamOneCurrent.specialattack*mult > self.teamTwoCurrent.specialdefense else 0
        self.teamTwo[self.teamTwoCurrentIdx][2] -= damage
      print(f"{self.teamOneCurrent.name.upper()} used {p1Attack} on {self.teamTwoCurrent.name.upper()} with {mult}x for {damage} damage")
      
    def teamTwoAttack(self):
      p2Attack = random.choice(["special attack", "physical attack"])
      
      if p2Attack == "physical attack":
        mult = 1
        damage = self.teamTwoCurrent.attack - self.teamOneCurrent.defense if self.teamTwoCurrent.attack > self.teamTwoCurrent.defense else 0
        self.teamOne[self.teamOneCurrentIdx][2] -= damage
      else:
        mult = 0
        typeFound = False
        for type in self.teamTwoCurrent.type:
          if self.teamOneCurrent.whenAttacked.get(type):
            typeFound = True
            mult = max(mult, self.teamOneCurrent.whenAttacked[type])
        if not typeFound:
          mult = 1
        damage = self.teamTwoCurrent.specialattack * mult - self.teamOneCurrent.specialdefense if self.teamTwoCurrent.specialattack*mult > self.teamOneCurrent.specialdefense else 0
        self.teamOne[self.teamOneCurrentIdx][2] -= damage
      print(f"{self.teamTwoCurrent.name.upper()} used {p2Attack} on {self.teamOneCurrent.name.upper()} with {mult}x for {damage} damage")
      
    def AttackAttack(self):
      for idx,[ID,_,_] in enumerate(self.teamOne):
        if ID == self.teamOneCurrent.ID:
          p1CurrentIdx = idx
      for idx,[ID,_,_] in enumerate(self.teamTwo):
        if ID == self.teamTwoCurrent.ID:
          p2CurrentIdx = idx
      if self.teamOneCurrent.speed > self.teamTwoCurrent.speed:
        self.teamOneAttack()
        if self.teamTwo[p2CurrentIdx][2]>0:
          self.teamTwoAttack()
      else:
        self.teamTwoAttack()
        if self.teamOne[p1CurrentIdx][2]>0:
          self.teamOneAttack()
    
    def SurrenderSurrender(self):
      print("BOTH TEAM LOSES")
      self.isBattling = False
    
    def P1Surrender(self):
      print("P1 LOST")
      self.isBattling = False
      self.winner = "teamTwo"
  
    def P2Surrender(self):
      print("P2 LOST")
      self.isBattling = False
      self.winner = "teamOne"
      
    def SwitchAttack(self, pkmID):
      self.setTeamOneCurrent(pkmID)
      self.teamTwoAttack()
    
    def AttackSwitch(self, pkmID):
      self.setTeamTwoCurrent(pkmID)
      self.teamOneAttack()
    
    def SwitchSwitch(self, pkmID1, pkmID2):
      self.setTeamOneCurrent(pkmID1)
      self.setTeamTwoCurrent(pkmID2)
    
    def resolveRound(self):
      teamOneLost = all(map(lambda x: x[2]<=0, self.teamOne))
      teamTwoLost = all(map(lambda x: x[2]<=0, self.teamTwo))
      if teamOneLost:
        self.P1Surrender()
      elif teamTwoLost:
        self.P2Surrender()
      