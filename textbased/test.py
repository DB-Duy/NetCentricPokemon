import pokemon
import APIRequest

pokemonGetter = APIRequest.PokemonGetter()

pokemon = pokemonGetter.getPokemon("charmander",15)
pokemon.giveExp(80000000)
pokemon.printPokemon()
