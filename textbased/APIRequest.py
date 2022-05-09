import requests
import json
import pokemon

class PokemonGetter:
  def __init__(self):
    self.PokemonURL = "https://pokeapi.co/api/v2/pokemon/"
    self.EvolutionURL = "https://pokeapi.co/api/v2/evolution-chain/"
    self.SpeciesURL = "https://pokeapi.co/api/v2/pokemon-species/"
    self.TypeURL = "https://pokeapi.co/api/v2/type/"

  def getPokemon(self, pokemonName: str, lvl: int =1, EV:int = 0.5):
    """Returns a pokemon object

    Args:
        pokemonName (str): the name of the Pokemon, not case sensitive
        lvl (int): level of the pokemon
    """
    pokemonInfo = self.getPokemonInfo(pokemonName)
    if pokemonInfo is None:
      return pokemonInfo
    pkm = pokemon.Pokemon(pokemonInfo, lvl, EV)
    return pkm
    
  def getPokemonInfo(self, pokemonName: str):
    """Requests API for pokemon and returns dict

    Args:
        pokemonName (str): pokemon name
    """
    response = requests.get(self.PokemonURL+pokemonName)
    if 200<= response.status_code < 300:
      info = response.json()
      info.update(self.getPokemonEvolutions(info))
      info.update(self.getPokemonDamageRelations(info))
      return info
    else:
      print("No pokemon with that name or connection failed") 
      return None
    
  def getTypeURL(self,pokemonName):
    response = requests.get(self.SpeciesURL+pokemonName)
    if 200<= response.status_code < 300:
      return response.json()['evolution_chain']['url']
    else:
      print("No pokemon with that name or connection failed") 
      return None
  
  def getPokemonDamageRelations(self, info):
    types=[]
    for type in info['types']:
      types.append(type['type']['name'])
    typedetails = []
    for type in types:
      response = requests.get(self.TypeURL+type)
      if not 200<=response.status_code<300:
        print("Connection failed")
        return None
      typedetails.append(response.json())
    return self.parseDamageRelations(typedetails)
    
  def parseDamageRelations(self, typedetails):
    relations = {"double_damage_from":2,"half_damage_from":0.5,"no_damage_from":0}
    multipliers = {}
    for detail in typedetails:
      detail = detail['damage_relations']
      for relation in relations:
        for type in detail[relation]:
          if multipliers.get(type['name']):
            multipliers[type['name']]*=relations[relation]
          else:
            multipliers[type['name']]=relations[relation]
    
    return {"damage_when_attacked":multipliers}
  
  def getEvolutionChainURL(self,pokemonName):
    response = requests.get(self.SpeciesURL+pokemonName)
    if 200<= response.status_code < 300:
      return response.json()['evolution_chain']['url']
    else:
      print("No pokemon with that name or connection failed") 
      return None
  
  def getPokemonEvolutions(self, info):
    """Requests API for pokemon and returns evo chain 
        Only evolutions by level is supported. If pokemon can't evolve by level it can't evolve

    Args:
        pokemonName (str): pokemonName

    Returns:
        dict: dicts with keys as levels and values as pokemon names
    """
    pokemonName = info['name']
    evolutionChainURL = self.getEvolutionChainURL(pokemonName)
    response = requests.get(evolutionChainURL)
    if not 200<= response.status_code < 300:
      print("Connection failed") 
      return None
    else:
      evos = response.json()['chain']
      evolution = {}
      if evos.get('evolves_to'):
        evos=evos['evolves_to'][0]
        while True:
          if evos['evolution_details'][0].get('min_level'):
            evolution[evos['evolution_details'][0]['min_level']] = evos['species']['name']
          if evos['evolves_to']==[]:
            break
          evos = evos['evolves_to'][0]

      return {'evolutions':evolution}