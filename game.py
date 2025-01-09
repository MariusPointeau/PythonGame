from dresseur import *
from map import *
from Engine import Renderer
from TerminalColor import color
from Math import *
import time
import os

potion_value = 25

class Fight(Enum):
    Null = 0
    Wild = 1
    Trainer = 2

class Cry(Enum):
    Growl = " growl\n"
    Roar = " roar\n"
    Watch = " watch you closely\n"

class Error(Enum):
    NoPotion = "\nThere is not enought potions to use\n"
    NoPokeball = "\nThere is not enought pokeball to use\n"
    NotEnoughtPokemon = "\nyou don't have that pokemon\n"
    AlreadyUsePokemon = "\nthis pokemon is already in battle\n"
    PokeballOnTrainer = "You can't take a trainer's pokemon\n"

class OverallMenu(Enum):
    MenuQuit = "\n0) quit"

class ObjectMenu(Enum):
    MenuEntry = "\nObjects\n"
    Potions = "\n1) potions : "
    Pokeballs = "\n2) pokeballs : "

class PokemonInPokeballFeedback(Enum):
    Try1 = "Oh no, he escaped\n"
    Try2 = "Oh no, close\n"
    Try3 = "Oh no.\n Come on one more pokeball and you've got it\n"
    GotIt = "Nice you got it\n"


class Game:

    def __init__(self, __pokemons, __map):
        self.clear = lambda: os.system('cls')

        self.playerPos = 13
        self.renderer = Renderer()
        self.player = Dresseur("Player 1")

        self.pokemons = __pokemons
        self.map = __map
        
        self.player.add_pokemon(self.AddRandomPokemons())
        self.player.add_pokemon(self.AddRandomPokemons())

        self.player.pokeball = 5
        self.fight_type = Fight.Null

        self.red_pokemon = Pokemon("None", 0, Type.Null)
        self.blue_pokemon = Pokemon("None", 0, Type.Null)

        self.close = False

        self.enemy_turn = False
    
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
            self.close = True
    
    def PlayerMoved(self, howMuch):
        self.map.tiles[self.playerPos].occupied = False
        self.map.tiles[self.playerPos].player = False
        self.playerPos += howMuch
        self.map.tiles[self.playerPos].occupied = True
        self.map.tiles[self.playerPos].player = True

        proba_wild_attack = random.randint(0,1)
        if(proba_wild_attack == 0):
            self.fight_type = Fight.Wild

    def Update(self):

        if(self.fight_type != Fight.Null):
            self.clear()
            self.Defi_Aleatoire()
        else:
            self.clear()
            self.renderer.Draw(self.DrawMap())
            self.GetKey()

    def AddRandomPokemons(self) -> Pokemon:
        random_pokemon = random.randint(0, len(self.pokemons)-1)
        return self.pokemons[random_pokemon].copy()

    def Defi_Aleatoire(self):

        dresseur2 = Dresseur("A Wild Pokemon")
        dresseur2.add_pokemon(self.AddRandomPokemons())
        dresseur2.money = random.randint(50, 250)
        dresseur2.taverne()

        text_to_print = "\n" + dresseur2.name + " appear\n\n"
        self.renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = dresseur2.pokemons[0].name + random.choice(list(Cry)).value
        self.renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = self.player.pokemons[0].name + " GO !\n\n"
        self.renderer.Draw(text_to_print)
        time.sleep(1.0)
        
        pokemon_index = 0
        for pokemon in self.player.pokemons:
            if(pokemon.life_points <= 0):
                pokemon_index += 1
            else:
                break

        self.red_pokemon = self.player.pokemons[pokemon_index]
        self.blue_pokemon = dresseur2.pokemons[0]

        while self.red_pokemon.dead == False and self.blue_pokemon.dead == False and self.fight_type == Fight.Wild:
            self.CombatPhase()

        if self.blue_pokemon.life_points <= 0 and self.fight_type == Fight.Wild:
            self.player.money += dresseur2.money
            self.red_pokemon.level_up(self.blue_pokemon.level + 5)
            self.player.Update()
            self.Run("You won against " + dresseur2.name)
    
    def DrawAttackMoves(self, red_pokemon):
        text_to_print = "Attack\n\n"
        i = 1
        for attack in red_pokemon.attacks:
            text_to_print += str(i) + ") " + attack.name + "\t damage : " + str(attack.damages) + "\t type : " + str(attack.type) + "\t usage : " + str(attack.usage) + "/" + str(attack.usage_limit) + "\n"
            i += 1
        return text_to_print
    
    def DrawObjectsInPocket(self):
        text_to_print = "\n" + ObjectMenu.MenuEntry.value
        text_to_print += OverallMenu.MenuQuit.value
        text_to_print += ObjectMenu.Potions.value + str(self.player.potions)
        text_to_print += ObjectMenu.Pokeballs.value + str(self.player.pokeball) + "\n"
        return text_to_print
    
    def CombatPhase(self):
        text_to_print = "\n" + self.blue_pokemon.name + " = " + str(self.blue_pokemon.life_points) + " hp\n\n"
        text_to_print += self.red_pokemon.name + " = " + str(self.red_pokemon.life_points) + " hp\n"
            
        text_to_print += "\nMoves :\n\n"
        text_to_print += "1) Attack\n"
        text_to_print += "2) Objects\n"
        text_to_print += "3) Pokemons\n"
        text_to_print += "4) Run\n"

        text_to_print += "\nenter the number for your move\n"
        self.renderer.Draw(text_to_print)
        move = Check_String_Input(input(""), 4)

        if(move == 1):
            self.AttackMenu()
        elif(move == 2):
            object_to_use = self.ObjectMenu()
        elif(move == 3):
            transition_pokemon = self.PokemonMenu()
            if(transition_pokemon.type != Type.Null):
                self.red_pokemon = transition_pokemon
        elif(move == 4):
            result = random.randint(0,100)
            if(result < 75):
                self.Run("\nYou escaped\n")
            else:
                self.enemy_turn = True

        if(self.fight_type != Fight.Null and self.enemy_turn):
            attackText = self.blue_pokemon.attack(random.choice(self.blue_pokemon.attacks), self.red_pokemon)
            self.renderer.Draw(attackText)
            self.enemy_turn = False
    
    def AttackMenu(self):
        self.renderer.Draw(OverallMenu.MenuQuit.value)
        self.renderer.Draw(self.DrawAttackMoves(self.red_pokemon))
        attack_selected = input("Attack to use : ")
        attack_selected = Check_String_Input(attack_selected, 4)
        if(attack_selected > 0):
            attackText = self.red_pokemon.attack(self.red_pokemon.attacks[attack_selected-1],self.blue_pokemon)
            self.renderer.Draw(attackText)
            self.enemy_turn = True

    def ObjectMenu(self):
        object_to_use = "\n"
        object_to_use = self.DrawObjectsInPocket()
        self.renderer.Draw(object_to_use + "\n")
        object_to_use = input("")
        object_to_use = Check_String_Input(object_to_use, 2)
        if(object_to_use == 1):
            if(self.player.potions > 0):
                pokemon_to_heal = self.PokemonMenu()
                if(pokemon_to_heal.type != Type.Null):
                    pokemon_to_heal.heal(potion_value)
                    self.enemy_turn = True
            else:
                self.renderer.Draw(Error.NoPotion.value)
                self.ObjectMenu()
        if(object_to_use == 2):
            result = self.LaunchPokeball()
            if(result):
                self.Run("You captured a wild " + self.blue_pokemon.name)
            else:
                self.enemy_turn = True
            
        
    def PokemonMenu(self):
        text_to_print = "Pokemons :\n" + OverallMenu.MenuQuit.value
        i = 1
        for pokemon in self.player.pokemons:
            text_to_print += "\n" + str(i) + ") " + pokemon.name + "\t hp : " + str(pokemon.life_points) + "\t type : " + str(pokemon.type)
            i += 1
        text_to_print += "\n"
        self.renderer.Draw(text_to_print)
        action = Check_String_Input(input(""), len(self.player.pokemons))
        if(action == 0):
            return Pokemon("None", 0, Type.Null)
        else:
            if(action > len(self.player.pokemons)):
                self.renderer.Draw(Error.NotEnoughtPokemon.value)
                self.PokemonMenu()
            elif(self.red_pokemon != self.player.pokemons[action-1]):
                self.enemy_turn = True
                return self.player.pokemons[action-1]
            else:
                self.renderer.Draw(Error.AlreadyUsePokemon.value)
                return self.red_pokemon

        pokemon_to_select = ""

    def LaunchPokeball(self):
        text_to_print = "\n"
        if(self.fight_type == Fight.Wild):
            catch = self.TryToCatch(75, "viewp")
            time.sleep(1.0)
            if(catch):
                catch = self.TryToCatch(65, "viewp")
                time.sleep(1.0)
                if(catch):
                    catch = self.TryToCatch(50, "tic")
                    time.sleep(1.0)
                    if(catch):
                        self.player.add_pokemon(self.blue_pokemon)
                        text_to_print += PokemonInPokeballFeedback.GotIt.value
                        self.renderer.Draw(text_to_print)
                        self.player.pokeball -= 1
                        return True
                    else:
                        text_to_print += PokemonInPokeballFeedback.Try3.value
                else:
                    text_to_print += PokemonInPokeballFeedback.Try2.value
            else:
                text_to_print += PokemonInPokeballFeedback.Try1.value
                        
        elif(self.fight_type == Fight.Trainer):
            text_to_print += Error.PokeballOnTrainer.value

        self.renderer.Draw(text_to_print)
        time.sleep(2.0)
        return False

    def Run(self, message):
        self.renderer.Draw(message)
        time.sleep(1.0)

        self.red_pokemon = Pokemon("None", 0, Type.Null)
        self.blue_pokemon = Pokemon("None", 0, Type.Null)
        self.fight_type = Fight.Null
        self.enemy_turn = False

    def TryToCatch(self, proba, message):
        catch = random.randrange(0,100)
        if(catch < proba):
            self.renderer.Draw("\n" + message + "\n")
            return True
        else:
            return False
        
    
    
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