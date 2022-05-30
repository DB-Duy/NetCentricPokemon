import json
from random import random
import requests
import threading
import logging 
import glob
import APIRequest
import uuid

## Constant URL
PokemonURL = "https://pokeapi.co/api/v2/pokemon/"
EvolutionURL = "https://pokeapi.co/api/v2/evolution-chain/"
SpeciesURL = "https://pokeapi.co/api/v2/pokemon-species/"
TypeURL = "https://pokeapi.co/api/v2/type/"

def getPokemonData(start, end):   
    data = []
    getter = APIRequest.PokemonGetter()
    for i in range(start,end+1):
        response = requests.get(PokemonURL+str(i))
        if 200<= response.status_code < 300:
            info =response.json()
            info.update(getter.getPokemonEvolutions(info))
            info.update(getter.getPokemonDamageRelations(info))
            cleanedInfo = getter.cleanInfo(info)
        data.append(cleanedInfo)
    with open(f"fetch_data/pokemon_{start}to{end}.json", "w") as write_file:
        json.dump(data, write_file)
      
def mergeAllJSONFiles():
    result = []
    for f in glob.glob("fetch_data/*.json"):
        with open(f,"r") as infile:
            print(f)
            load = json.loads(infile.read())
            if load:
                result +=load
    JSONdata = result
    str_JSON = json.dumps(JSONdata)
    with open("fetch_data/pokemon_basic_info.json", "w") as outfile:
        json.dump(JSONdata,outfile)

## Multi-threading 
# Fetch all basic data about Pokemon
begin, end = (1,500)
tasks = []
x = begin
iteration = 5
while x < end:
    if x + iteration > end:
        iteration = end - x 
    tasks.append((x, x + iteration))
    x = x + iteration + 1 
print(tasks)
threads = list()
for task in tasks:
    x = threading.Thread(target=getPokemonData, args=(task[0],task[1]))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    logging.info("Main    : before joining thread %d.", index)
    thread.join()
    logging.info("Main    : thread %d done", index)
mergeAllJSONFiles()