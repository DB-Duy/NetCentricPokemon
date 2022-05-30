import APIRequest
import json


class Pokemon:
    def __init__(self, pokemonInfo, leftOverEXP=0):
        """Creates a pokemon

        Args:
            pokemonInfo (dict):  Dict containing pokemon attributes
            lvl (int): the pokemon's level
            EV (float): the pokemon's EV - Default is 0.5
            leftOverEXP(int): the exp to give pokemon
        """
        self.pokemonInfo = pokemonInfo
        if type(pokemonInfo) != type({}):
            raise TypeError('Input dict only')
        self.level = 1
        self.type = []
        self.currentEXP = 0
        self.__parseInfo(pokemonInfo)
        self.giveExp(leftOverEXP)

    def __parseInfo(self, pokemonInfo):
        self.ID = pokemonInfo['PokemonID']
        self.EV = pokemonInfo['EV']
        self.base_experience = pokemonInfo['base_experience']
        self.name = pokemonInfo['name']
        self.evolutions = pokemonInfo['evolutions']
        self.whenAttacked = pokemonInfo['damage_when_attacked']
        for type in pokemonInfo['types']:
            self.type.append(type['type']['name'])
        self.spriteURL = pokemonInfo['sprites']['front_default']
        for stat in pokemonInfo['stats']:
            statName = "base_"+stat['stat']['name'].replace("-", "")
            exec(f"self.{ statName }={stat['base_stat']}")
        self.APIId = pokemonInfo['id']
        self.levelTo(pokemonInfo['level'])

    def printPokemon(self):
        print("-"*10)
        print(f"ID: {self.ID}")
        print(f"SpriteURL: {self.spriteURL}")
        print("-"*10)
        print(f"Name: {self.name.upper()}")
        print(f"Level: {self.level}")
        print(f"EXP to next Level: {self.EXPToLevelUp-self.currentEXP:,}")
        t = self.type[0]
        if len(self.type) > 1:
            for i in range(1, len(self.type)):
                t += '-'
                t += self.type[i]
        print(f"Type(s): {t.upper()}")
        print("-"*10)
        print(f"HP: {self.hp:,}")
        print(f"Spd: {self.speed:,}")
        print(f"Atk: {self.attack:,}")
        print(f"Sp.Atk: {self.specialattack:,}")
        print(f"Def: {self.defense:,}")
        print(f"Sp.Def: {self.specialdefense:,}")
        print("-"*10)

    def levelTo(self, lvl):
        if lvl > 100:
            lvl = 100
        self.level = lvl
        self.__checkEvolve()
        self.__updateStats()
        self.updateInfo()
        self.EXPToLevelUp = self.base_experience * (2**self.level)
        
    def getEXPReward(self):
        return self.EXPToLevelUp

    def __updateStats(self):
        mult = (1+self.EV)**self.level
        self.hp = int(self.base_hp * mult)
        self.speed = int(self.base_speed * mult)
        self.attack = int(self.base_attack * mult)
        self.specialattack = int(self.base_specialattack * mult)
        self.defense = int(self.base_defense * mult)
        self.specialdefense = int(self.base_specialdefense * mult)

    def __checkEvolve(self):
        evos = sorted([[int(lvl), self.evolutions[lvl]]
                      for lvl in self.evolutions], key=lambda x: str(x[0]), reverse=True)
        for evo in evos:
            if self.level >= evo[0] and self.name == evo[1]:
                break
            elif self.level >= evo[0] and self.name != evo[1]:
                pkmGetter = APIRequest.PokemonGetter()
                evolvedPkmInfo = pkmGetter.getPokemonInfo(evo[1])
                evolvedPkmInfo.update({"PokemonID":self.ID, "level":self.level, "EV": self.EV})
                self.__init__(evolvedPkmInfo, self.currentEXP)
                break

    def giveExp(self, exp):
        self.currentEXP += exp
        while self.currentEXP >= self.EXPToLevelUp:
            self.currentEXP -= self.EXPToLevelUp
            self.levelTo(self.level+1)
        self.updateInfo()
    
    def getPokemonInfo(self):
        self.updateInfo()
        return self.pokemonInfo
    
    def updateInfo(self):
        self.pokemonInfo.update({"currentEXP":self.currentEXP,"level":self.level,"EV":self.EV})


class PokeTeam:
    def __init__(self, pokemonList=[]):
        self.pokemonList = []
        self.battleList = []
        self.addPokemon(pokemonList)
        
    def addPokemon(self,pokemon):
        if type(pokemon) == list:
            for pkm in pokemon:
                if self.checkPokemonInList(pkm.ID):
                    print("Pokemon already in team")
                    continue
                if self.numberOfPokemons()>=200:
                    print("Pokemon limit exceeded, please remove some before adding")
                    return
                self.pokemonList.append(pkm)
        if type(pokemon) == Pokemon:
            if self.checkPokemonInList(pokemon.ID):
                    print("Pokemon already in team")
                    return
            if self.numberOfPokemons()>=200:
                    print("Pokemon limit exceeded, please remove some before adding")
                    return
            self.pokemonList.append(pokemon)
            
    def removePokemon(self, pokemonID:str):
        for idx,pkm in enumerate(self.pokemonList):
            if pkm.ID == pokemonID:
                self.pokemonList.pop(idx)
        self.removeFromBattleList(pokemonID)
    
    def removeFromBattleList(self, pokemonID:str):
        for idx,pkmID in enumerate(self.battleList):
            if pkmID == pokemonID:
                self.battleList.pop(idx)
            
    def selectPokemonForBattle(self, pokemonID:str):
        if pokemonID in self.battleList:
            print("Pokemon already in battlelist")
            return
        if not self.checkPokemonInList(pokemonID):
            print("Pokemon not in team")
            return
        if len(self.battleList)<3: 
                self.battleList.append(pokemonID)
        elif len(self.battleList)==3:
            print("Please replace Pokemon")
            validInput = ["1","2","3","4"]
            for idx,name in enumerate(self.getBattlePokemonNames()):
                print(f"{idx+1}. {name}   ",end="")
            print("4. Cancel")
            userInput = ""
            while userInput not in validInput:
                userInput = input()
            if userInput == "4":
                return
            else:
                self.battleList[int(userInput)-1]=pokemonID
            
    def getPokemonFromID(self, pokemonID)->Pokemon:
        for pkm in self.pokemonList:
            if pkm.ID == pokemonID:
                return pkm
        
    def checkPokemonInList(self,pokemonID):
        for pkm in self.pokemonList:
            if pokemonID == pkm.ID:
                return True
        return False
                
    def numberOfPokemons(self):
        return len(self.pokemonList)
    
    def getPokemonInfos(self):
        for pkm in self.pokemonList:
            pkm.updateInfo()
        pokemonInfos = [pkm.getPokemonInfo() for pkm in self.pokemonList]
        battleTeam = [pkmID for pkmID in self.battleList]
        if pokemonInfos:
            return { "team": pokemonInfos, "battle": battleTeam }

    def loadPokemons(self, pokemonInfos):
        team = [Pokemon(info) for info in pokemonInfos['team']]
        self.addPokemon(team)
        for pkmID in pokemonInfos['battle']:
            self.selectPokemonForBattle(pkmID)
        
    def getPokemonNames(self):
        return [pkm.name for pkm in self.pokemonList]
    
    def getBattlePokemonNames(self):
        return [self.getPokemonFromID(ID).name for ID in self.battleList]
    
    def printAllPokemon(self):
        for pkm in self.pokemonList:
            pkm.printPokemon()
            
    def printBattlePokemon(self):
        for pkmID in self.battleList:
            pkm = self.getPokemonFromID(pkmID)
            pkm.printPokemon()
