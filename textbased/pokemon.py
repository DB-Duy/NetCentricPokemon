
class Pokemon:
  def __init__(self, pokemonInfo):
    """Creates a pokemon

    Args:
        pokemonInfo (dict):  Dict containing pokemon attributes
    """
    if type(pokemonInfo) != type({}):
      raise TypeError('Input dict only')
    self.level = 5
    self.type = []
    self.parseInfo(pokemonInfo) 
    self.currentHP = self.base_hp
    self.EV = 0.5
    self.currentEXP = 0
    
  def parseInfo(self, pokemonInfo):
    self.base_experience = pokemonInfo['base_experience']
    self.name=pokemonInfo['name']
    self.evolutions = pokemonInfo['evolutions']
    for type in pokemonInfo['types']:
      self.type.append(type['type']['name'])
    self.spriteURL = pokemonInfo['sprites']['front_default']
    for stat in pokemonInfo['stats']:
      statName = "base_"+stat['stat']['name'].replace("-","")
      exec(f"self.{ statName }={stat['base_stat']}")
    self.id = pokemonInfo['id']
  
  def printPokemon(self):
    print(f"Name: {self.name.upper()}")
    print(f"Level: {self.level}")
    t=self.type[0]
    if len(self.type)>1:
      for i in range(1,len(self.type)):
        t+='-'
        t+=self.type[i]
    print(f"Type(s): {t.upper()}")
    print("-"*10)
    print(f"HP: {self.base_hp}")
    print(f"Spd: {self.base_speed}")
    print(f"Atk: {self.base_attack}")
    print(f"Sp.Atk: {self.base_specialattack}")
    print(f"HP: {self.base_specialdefense}")
    
  def lvlUp(self):
    self.level+=1

  
  def giveExp(self, exp):
    if self.level == 100:
      return
    if self.currentEXP + exp >= self.base_experience:
      self.lvlUp()
      self.currentEXP = self.currentEXP+exp -self.base_experience