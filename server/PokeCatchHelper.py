from APIRequest import *
import requests
import random
import json
import time 
from settings import *
from pokemon import *
import pickle
def spawn_pokemon_wave(wave_num):
    pokemon_wave = {}
    pokemon_wave_packet = {}
    with open("fetch_data/pokemon_basic_info.json", "r") as f:
        data = json.load(f)
    for i in range(0,50):
        pkm = data[random.randint(1,299)]
        pkm.update({"level":random.randint(1,10), "EV":random.uniform(0.5,1),"PokemonID":i,"waveId": wave_num })
        pkm = Pokemon(pkm)
        pokemon_wave.update({pkm.ID : pkm})
        pokemon_wave_packet.update({pkm.ID: (pkm.spriteURL,random.randrange(1,MAP_WIDTH-1),random.randrange(1,MAP_HEIGHT-1))})
    # with open("spawn_wave.json","w") as f:
    #     json.dump(pokemon_wave,f)
    return pokemon_wave, pokemon_wave_packet
        

    # C = PokemonGetter()
    # info = C.getPokemonInfo("1")
    # print(info)

def catch_pokemon(Pokemons,Pokemons_packet, pokemonId):
    for waveId in Pokemons_packet.keys():
        if waveId != "isPokemonPacket":  
            if pokemonId in Pokemons_packet[waveId]:
                data = Pokemons[waveId][pokemonId]
                del Pokemons[waveId][pokemonId]
                del Pokemons_packet[waveId][pokemonId]
                print("Successfully caught ")
                return data.__dict__
    print("Pokemon not found")
    return {} 
# def check_player_collide_pokemon():
#     pass
def thread_spawn_wave(Pokemons,Pokemons_packet, Players):
    id = 1 
    while True:
        if not Players:
            continue
        if  id >=6:
            del Pokemons[id - 5]
            del Pokemons_packet[id - 5]
        Pokemons[id], Pokemons_packet[id] = spawn_pokemon_wave(id)
        print("New wave spawn id: ", id)
        for wave in Pokemons.keys():
            print(f'Wave {wave} : {len(Pokemons[wave])}')

        
        id += 1
        time.sleep(60) 

# Pokemons = {}
# Pokemons_packet = {"isPokemonPacket": True}
# Pokemons[1], Pokemons_packet[1] = spawn_pokemon_wave(1)
# Pokemons[2], Pokemons_packet[2] = spawn_pokemon_wave(2)
# print(len(Pokemons[1]))
# print("Before catch ", len(Pokemons[1]), len(Pokemons_packet[1]))
# pkm = catch_pokemon(Pokemons,Pokemons_packet,1)
# print("After catch ", len(Pokemons[1]), len(Pokemons_packet[1]))
# print("Catched ",pkm)