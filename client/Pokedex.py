import requests 
import json

pk=requests.get("https://pokedex.org/#/pokemon/1").text
print(pk)