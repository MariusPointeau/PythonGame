from pokemon import *

class Dresseur:

    def __init__(self, __name):
        self.name = __name
        self.money = 0
        self.defeated = False
        self.pokemons = []
        self.potions = 0
        self.pokeball = 0

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
            self.defeated = False
        return "\nAll your pokemons have been healed\n"

    def AutoSelectAlivePokemon(self):
        pokemon_index = 0
        for pokemon in self.pokemons:
            if(pokemon.life_points <= 0):
                pokemon_index += 1
            else:
                break
        return self.pokemons[pokemon_index]

    def Update(self):
        if(self.pokemons[0].dead):
            lost = False
            for pokemon in self.pokemons:
                if(pokemon.dead):
                    lost = True
                    continue
                else:
                    lost = False
                    break
            
            self.defeated = lost

    def RandomPokemon(self) -> Pokemon:
        return self.pokemons[random.randint(0, len(self.pokemons)-1)]

    def HigherLifePokemon(self) -> Pokemon:
        chosen_pokemon = Pokemon("", 0)
        for pokemon in self.pokemons:
            if(pokemon.life_points > chosen_pokemon.life_points):
                chosen_pokemon = pokemon
        return chosen_pokemon