import APIRequest


class Pokemon:
    def __init__(self, pokemonInfo, lvl=1, EV=0.5, leftOverEXP=0):
        """Creates a pokemon

        Args:
            pokemonInfo (dict):  Dict containing pokemon attributes
            lvl (int): the pokemon's level
            EV (float): the pokemon's EV - Default is 0.5
        """
        if type(pokemonInfo) != type({}):
            raise TypeError('Input dict only')
        self.level = 1
        self.type = []
        self.parseInfo(pokemonInfo)
        self.EV = EV
        self.levelTo(lvl)
        self.currentEXP = 0
        self.giveExp(leftOverEXP)
        self.currentHP = self.hp

    def parseInfo(self, pokemonInfo):
        self.base_experience = pokemonInfo['base_experience']
        self.name = pokemonInfo['name']
        self.evolutions = pokemonInfo['evolutions']
        for type in pokemonInfo['types']:
            self.type.append(type['type']['name'])
        self.spriteURL = pokemonInfo['sprites']['front_default']
        for stat in pokemonInfo['stats']:
            statName = "base_"+stat['stat']['name'].replace("-", "")
            exec(f"self.{ statName }={stat['base_stat']}")
        self.id = pokemonInfo['id']

    def printPokemon(self):
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
        self.checkEvolve()
        self.updateStats()
        self.EXPToLevelUp = self.base_experience * (2**self.level)

    def updateStats(self):
        mult = (1+self.EV)**self.level
        self.hp = int(self.base_hp * mult)
        self.speed = int(self.base_speed * mult)
        self.attack = int(self.base_attack * mult)
        self.specialattack = int(self.base_specialattack * mult)
        self.defense = int(self.base_defense * mult)
        self.specialdefense = int(self.base_specialdefense * mult)

    def checkEvolve(self):
        evos = sorted([[lvl, self.evolutions[lvl]]
                      for lvl in self.evolutions], key=lambda x: x[0], reverse=True)
        for evo in evos:
            if self.level >= evo[0] and self.name == evo[1]:
                break
            elif self.level >= evo[0] and self.name != evo[1]:
                pkmGetter = APIRequest.PokemonGetter()
                evolvedPkmInfo = pkmGetter.getPokemonInfo(evo[1])
                self.__init__(evolvedPkmInfo, self.level,
                              self.EV, self.currentEXP)
                break

    def giveExp(self, exp):
        self.currentEXP += exp
        EXPtoLevel = self.EXPToLevelUp
        levelsUp = 0
        while self.currentEXP >= self.EXPToLevelUp:
            self.currentEXP -= EXPtoLevel
            EXPtoLevel *= 2
            levelsUp += 1
        self.levelTo(self.level+levelsUp)

    def isAlive(self):
        return self.currentHP > 0
