from dresseur import *
from map import *
from Engine import Renderer
from TerminalColor import color
import time

class Game:
    map = Map()
    pokemons = []
    playerPos = 13
    renderer = Renderer()
    player = Dresseur("Player 1")

    close = False

    def __init__(self, __pokemons, __map):
        self.pokemons = __pokemons
        self.map = __map
        self.player.add_pokemon(random.choice(self.pokemons))
    
    def DrawMap(self):
        return self.map.__str__()
    
    def SpawmColletible(self):
        tile = self.map.GetRandomTile()
        tile.occupied = True
        tile.potion = True

    def GetKey(self):
        direction = input("Direction (WASD) = ")
        if(direction == "w" or direction == "W" or direction == "z" or direction == "Z"):
            self.PlayerMoved(-5)
        elif(direction == "s" or direction == "S"):
            self.PlayerMoved(5)
        elif(direction == "a" or direction == "A" or direction == "q" or direction == "Q"):
            self.PlayerMoved(-1)
        elif(direction == "d" or direction == "D"):
            self.PlayerMoved(1)
        elif(direction == "quit"):
            close = True
    
    def PlayerMoved(self, howMuch):
        self.map.tiles[self.playerPos].occupied = False
        self.map.tiles[self.playerPos].player = False
        self.playerPos += howMuch
        self.map.tiles[self.playerPos].occupied = True
        self.map.tiles[self.playerPos].player = True

    def Update(self):
        self.Defi_Aleatoire()
        self.close = True
        print("\033c")


    def Defi_Aleatoire(self):

        dresseur2 = Dresseur("A Wild Pokemon")
        dresseur2.add_pokemon(random.choice(self.pokemons))
        dresseur2.taverne()

        text_to_print = dresseur2.name + " appear\n\n"
        self.renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = dresseur2.pokemons[0].name + " growl\n\n"
        self.renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = self.player.pokemons[0].name + " GO !\n\n"
        self.renderer.Draw(text_to_print)
        time.sleep(1.0)
        

        red_pokemon = self.player.pokemons[0]
        blue_pokemon = dresseur2.pokemons[0]

        while red_pokemon.dead == False and blue_pokemon.dead == False:
            text_to_print = blue_pokemon.name + " = " + str(blue_pokemon.life_points) + " hp\n\n"
            text_to_print += red_pokemon.name + " = " + str(red_pokemon.life_points) + " hp\n\n"
            
            text_to_print += "Moves :\n\n"
            text_to_print += "1) Attack\n"
            text_to_print += "2) Use potion : +25 hp\n"
            text_to_print += "3) Throw pokeball\n"
            text_to_print += "4) Run\n\n"

            text_to_print += "enter the number for your move\n\n"
            self.renderer.Draw(text_to_print)
            move = int(input(""))

            if(move == 1):
                self.renderer.Draw(self.DrawAttackMoves(red_pokemon))


    
        if red_pokemon.life_points <= 0:
            dresseur2.experience += 1
            blue_pokemon.level_up(5)
        
        elif blue_pokemon.life_points <= 0:
            self.experience += 1
            red_pokemon.level_up(5)
    
    def DrawAttackMoves(self, red_pokemon):
        text_to_print = "Attack\n\n"
        i = 1
        for attack in red_pokemon.attacks:
            text_to_print += str(i) + ") " + attack.name + "\t damage : " + str(attack.damages) + "\t type : " + str(attack.type) + "\t usage : " + str(attack.usage) + "/" + str(attack.usage_limit) + "\n\n"
        return text_to_print

    
    '''def Defi_Deterministe(self, dresseur2):

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
            red_pokemon.level_up(5)'''