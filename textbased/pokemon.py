
class Pokemon:
  def __init__(self, pokemonInfo, evolutionInfo):
    """Creates a pokemon

    Args:
        pokemonInfo (dict):  Dict containing pokemon attributes
    """
    if type(pokemonInfo) != type({}):
      raise TypeError('Input dict only')
    self.parseInfo(pokemonInfo, evolutionInfo)
    
  def parseInfo(self, pokemonInfo):
    self.name=pokemonInfo['name']
    for type in pokemonInfo['types']:
      self.type.append(type['type']['name'])
    self.spriteURL = pokemonInfo['sprites']['front_default']
    for stat in pokemonInfo['stats']:
      exec(f"self.{stat['stat']['name']}={stat['base_stat']}")
    self.id = pokemonInfo['id']