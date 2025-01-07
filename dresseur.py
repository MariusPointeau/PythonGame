from pokemon import *

class Dresseur:

    def __init__(self, __name, __experience, __level):
        self.name = __name
        self.experience = __experience
        self.level = __level
        self.defeated = False
        self.pokemons = []
    
    def __str__(self):
        return self.name + " has " + str(self.experience) + " xp points and is level " + str(self.level)

    def add_pokemon(self, pokemon):
        if len(self.pokemons) < 6:
            self.pokemons.append(pokemon)

    def taverne(self):
        for pokemon in self.pokemons:
            pokemon.life_points = pokemon.maxlife_points
            pokemon.dead = False
            for attack in pokemon.attacks:
                attack.usage = 0
    
    def Update(self):
        if self.experience >= 10:
            self.level += 1
            self.experience = 0
        
        if(self.pokemons[0].dead):
            lost = False
            for pokemon in self.pokemons:
                if(pokemon.dead):
                    lost = True
                    continue
                else:
                    lost = False
                    break
            
            if(lost):
                self.defeated = True
    
    def RandomPokemon(self) -> Pokemon:
        return self.pokemons[random.randint(0, len(self.pokemons)-1)]

    def HigherLifePokemon(self) -> Pokemon:
        chosen_pokemon = Pokemon("", 0)
        for pokemon in self.pokemons:
            if(pokemon.life_points > chosen_pokemon.life_points):
                chosen_pokemon = pokemon
        return chosen_pokemon

    def Defi_Aleatoire(self, dresseur2):
        self.taverne()
        dresseur2.taverne()

        red_pokemon = self.RandomPokemon()
        blue_pokemon = dresseur2.RandomPokemon()

        while red_pokemon.dead == False and blue_pokemon.dead == False:
            if random.randint(0,1) == 0:
                red_pokemon.attack(blue_pokemon)
                blue_pokemon.attack(red_pokemon)
            else:
                blue_pokemon.attack(red_pokemon)
                red_pokemon.attack(blue_pokemon)
    
        if red_pokemon.life_points <= 0:
            dresseur2.experience += 1
            blue_pokemon.level_up(5)
        
        elif blue_pokemon.life_points <= 0:
            self.experience += 1
            red_pokemon.level_up(5)
        
    def Arene1(self, dresseur2):
        counter = 0
        while counter < 100:
            self.Defi_Aleatoire(dresseur2)
            self.Update()
            dresseur2.Update()
            print(self)
            print(dresseur2.__str__() + "\n\n")
            counter += 1
        
        if(self.level > dresseur2.level):
            print(self.name + " has won the arena")
        elif(self.level < dresseur2.level):
            print(dresseur2.name + " has won the arena")
        elif(self.experience > dresseur2.experience):
            print(self.name + " has won the arena")
        else:
            print(dresseur2.name + " has won the arena")

    def Defi_Deterministe(self, dresseur2):

        red_pokemon = self.HigherLifePokemon()
        blue_pokemon = dresseur2.HigherLifePokemon()

        while red_pokemon.dead == False and blue_pokemon.dead == False:
            if random.randint(0,1) == 0:
                red_pokemon.attack(blue_pokemon)
                blue_pokemon.attack(red_pokemon)
            else:
                blue_pokemon.attack(red_pokemon)
                red_pokemon.attack(blue_pokemon)
    
        if red_pokemon.life_points <= 0:
            dresseur2.experience += 1
            blue_pokemon.level_up(5)
        
        elif blue_pokemon.life_points <= 0:
            self.experience += 1
            red_pokemon.level_up(5)
    
    def Arena2(self, dresseur2):
        counter = 0
        while counter < 100 and not self.defeated and not dresseur2.defeated:
            self.Defi_Deterministe(dresseur2)
            self.Update()
            dresseur2.Update()
            print(self)
            print(dresseur2.__str__() + "\n\n")
            counter += 1
        
        if(self.level > dresseur2.level):
            print(self.name + " has won the arena")
        elif(self.level < dresseur2.level):
            print(dresseur2.name + " has won the arena")
        elif(self.experience > dresseur2.experience):
            print(self.name + " has won the arena")
        else:
            print(dresseur2.name + " has won the arena")