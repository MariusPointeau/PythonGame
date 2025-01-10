from dresseur import *
from map import *
from Engine import Renderer
from TerminalColor import color
from Math import *
from Dialogue import *
import time
import os

potion_value = 120

class Action(Enum):
    Null = 0
    Wild = 1
    Trainer = 2
    Talk = 3

class Cry(Enum):
    Growl = " growl\n"
    Roar = " roar\n"
    Watch = " watch you closely\n"

class Error(Enum):
    NoPotion = "\nThere is not enought potions to use\n"
    NoPokeball = "\nThere is not enought pokeball to use\n"
    NotEnoughtPokemon = "\nyou don't have that pokemon\n"
    AlreadyUsePokemon = "\nthis pokemon is already in battle\n"
    PokeballOnTrainer = "\nYou can't take a trainer's pokemon\n"
    SelectedPokemonDead = "\nYou have to chose another pokemon\n"
    TryToEscapeTrainer = "\nYou try to flee ?\nYou coward\n"
    TrainerHealedPokemon = " used a potion for "

class TrainerName(Enum):
    Scout = "Scout Philibert"
    Gamin = "Gamin Matheo"
    Pecheur = "Pecheur Marco"
    Nageuse = "Nageuse Sophie"
    Bob = "Bob"

class OverallMenu(Enum):
    MenuQuit = "\n0) quit"

class ObjectMenu(Enum):
    MenuEntry = "\nObjects\n"
    Potions = "\n1) potions : "
    Pokeballs = "\n2) pokeballs : "

class PokemonInPokeballFeedback(Enum):
    Try1 = "\nOh no, he escaped\n"
    Try2 = "\nOh no, close\n"
    Try3 = "\nOh no !\nCome on one more pokeball and you've got it\n"
    GotIt = "\nNice you got it\n"


class Game:

    def __init__(self, __pokemons, __map):
        self.clear = lambda: os.system('cls')

        self.playerPos = 13
        self.player = Dresseur("Player 1")

        self.pokemons = __pokemons
        self.map = __map
        
        self.player.add_pokemon(self.AddRandomPokemons())
        self.player.add_pokemon(self.AddRandomPokemons())

        self.player.pokeball = 5
        self.action_type = Action.Null

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

    def SpawnTrainer(self, nb_trainer):
        for i in range(0, nb_trainer):
            tile = self.map.GetRandomTile()
            tile.occupied = True
            tile.trainer = True

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
        tile = self.map.tiles[self.playerPos + howMuch]
        if(tile.occupied):
            if(tile.potion):
                self.player.potions += 1
            elif(tile.trainer):
                self.action_type = Action.Talk
                return
        self.map.tiles[self.playerPos].occupied = False
        self.map.tiles[self.playerPos].player = False
        self.playerPos += howMuch
        self.map.tiles[self.playerPos].occupied = True
        self.map.tiles[self.playerPos].player = True

        proba_wild_attack = random.randint(0,2)
        if(proba_wild_attack == 0):
            self.action_type = Action.Wild

    def Update(self):
        self.clear()
        if(self.action_type != Action.Null):
            if(self.action_type == Action.Talk):
                dialogue = Dialogue(random.choice(list(TrainerName)).value, random.randint(1,3))
                response = dialogue.Conversation()
                if(response):
                    self.action_type = Action.Trainer
                else:
                    self.action_type = Action.Null
                time.sleep(2.0)
            
            if(self.action_type == Action.Wild):
                self.Defi_Aleatoire()
            elif(self.action_type == Action.Trainer):
                self.Challenge_Trainer(dialogue.interaction_name, dialogue.nb_pokemon)
        else:
            Renderer.Draw(self.DrawMap())
            self.GetKey()

    def AddRandomPokemons(self) -> Pokemon:
        random_pokemon = random.randint(0, len(self.pokemons)-1)
        return self.pokemons[random_pokemon].copy()

    def Defi_Aleatoire(self):
        dresseur2 = Dresseur("A Wild Pokemon")
        dresseur2.add_pokemon(self.AddRandomPokemons())
        dresseur2.money = random.randint(50, 250)
        dresseur2.potions = random.randint(0,2)
        dresseur2.taverne()

        text_to_print = "\n" + dresseur2.name + " appear\n\n"
        Renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = dresseur2.pokemons[0].name + random.choice(list(Cry)).value
        Renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = self.player.pokemons[0].name + " GO !\n\n"
        Renderer.Draw(text_to_print)
        time.sleep(1.0)

        self.red_pokemon = self.player.AutoSelectAlivePokemon()
        self.blue_pokemon = dresseur2.pokemons[0]

        while self.player.defeated == False and dresseur2.defeated == False and self.action_type == Action.Wild:
            self.CombatPhase(dresseur2)

        if(dresseur2.defeated and self.action_type != Action.Null):
            self.player.money += dresseur2.money
            self.Run("You won against " + dresseur2.name + " and gained " + str(dresseur2.money))
            time.sleep(1.0)
        
        if self.player.defeated and self.action_type != Action.Null:
            self.Run("You lost against " + dresseur2.name)
            Renderer.Draw(self.player.taverne())
            time.sleep(1.0)
    
    def Challenge_Trainer(self, trainer_name, pokemon_number):
        dresseur2 = Dresseur(trainer_name)
        for i in range(0,pokemon_number):
            dresseur2.add_pokemon(self.AddRandomPokemons())
        dresseur2.money = random.randint(50, 250)
        dresseur2.taverne()

        if(trainer_name == TrainerName.Bob.value):
            result = random.randint(0,2)
            if(result == 0):
                for i in range(pokemon_number):
                    dresseur2.pokemons[i].name = TrainerName.Bob.value

        text_to_print = "\nYou challenged " + dresseur2.name + "\n"
        Renderer.Draw(text_to_print)
        time.sleep(1.0)

        text_to_print = "\n" + dresseur2.name + " chose " + dresseur2.pokemons[0].name + "\n"
        Renderer.Draw(text_to_print)
        time.sleep(1.0)

        pokemon_index = 0
        for pokemon in self.player.pokemons:
            if(pokemon.life_points <= 0):
                pokemon_index += 1
            else:
                break

        self.red_pokemon = self.player.pokemons[pokemon_index]

        text_to_print = self.red_pokemon.name + " GO !\n"
        Renderer.Draw(text_to_print)
        time.sleep(1.0)
        
        self.blue_pokemon = dresseur2.pokemons[0]

        while self.player.defeated == False and dresseur2.defeated == False and self.action_type == Action.Trainer:
            self.CombatPhase(dresseur2)

        if(dresseur2.defeated and self.action_type != Action.Null):
            self.player.money += dresseur2.money
            self.Run("You won against " + dresseur2.name + " and gained " + str(dresseur2.money))
            time.sleep(1.0)
        
        if self.player.defeated and self.action_type != Action.Null:
            self.Run("You lost against " + dresseur2.name)
            Renderer.Draw(self.player.taverne())
            time.sleep(1.0)
    
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
    
    def CombatPhase(self, dresseur2):
        text_to_print = "\n" + self.blue_pokemon.name + " = " + str(self.blue_pokemon.life_points) + " hp\n\n"
        text_to_print += self.red_pokemon.name + " = " + str(self.red_pokemon.life_points) + " hp\n"
            
        text_to_print += "\nMoves :\n\n"
        text_to_print += "1) Attack\n"
        text_to_print += "2) Objects\n"
        text_to_print += "3) Pokemons\n"
        text_to_print += "4) Run\n"

        text_to_print += "\nenter the number for your move\n"
        Renderer.Draw(text_to_print)
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
            if(self.action_type == Action.Wild):    
                result = random.randint(0,100)
                if(result < 75):
                    self.Run("\nYou escaped\n")
                else:
                    self.enemy_turn = True
            else:
                Renderer.Draw(Error.TryToEscapeTrainer.value)
                time.sleep(2.0)
                return
        else:
            return

        if(self.action_type != Action.Null and self.enemy_turn):
            attackText = ""
            if(self.action_type == Action.Wild):
                attackText = self.blue_pokemon.attack(self.EnemyChooseAttack(), self.red_pokemon)
            elif(self.action_type == Action.Trainer):
                if(self.blue_pokemon.life_points <= int(self.blue_pokemon.maxlife_points/2) and dresseur2.potions > 0):
                    self.blue_pokemon.heal(potion_value)
                    dresseur2.potions -= 1
                    attackText = "\n" + dresseur2.name + Error.TrainerHealedPokemon.value + self.blue_pokemon.name + "\n"
                else:
                    attackText = self.blue_pokemon.attack(self.EnemyChooseAttack(), self.red_pokemon)
            Renderer.Draw(attackText)
            self.enemy_turn = False
        
        if self.blue_pokemon.life_points <= 0:
            self.red_pokemon.level_up(self.blue_pokemon.level + 5)
            dresseur2.Update()
            if(not dresseur2.defeated):
                self.blue_pokemon = dresseur2.AutoSelectAlivePokemon()

        elif self.red_pokemon.life_points <= 0:
            self.player.Update()
            if(not self.player.defeated):
                self.red_pokemon = self.PokemonMenu()
    
    def EnemyChooseAttack(self) -> Attack:
        if(self.action_type == Action.Wild):
            return self.blue_pokemon.GetRandomAttack()
        elif(self.action_type == Action.Trainer):
            attack_to_use = self.blue_pokemon.GetRandomAttack()
            for attack in self.blue_pokemon.attacks:
                if(Type.Adventage(attack.type, self.red_pokemon.type) and attack.damages >= attack_to_use.damages and attack.usage < attack.usage_limit):
                    attack_to_use = attack
                if(attack.damages * Type.Adventage(attack.type, self.red_pokemon.type) >= self.red_pokemon.life_points):
                    attack_to_use = attack
                    break
            return attack_to_use

    
    def AttackMenu(self):
        Renderer.Draw(OverallMenu.MenuQuit.value)
        Renderer.Draw(self.DrawAttackMoves(self.red_pokemon))
        attack_selected = input("Attack to use : ")
        attack_selected = Check_String_Input(attack_selected, 4)
        if(attack_selected > 0):
            attackText = self.red_pokemon.attack(self.red_pokemon.attacks[attack_selected-1],self.blue_pokemon)
            Renderer.Draw(attackText)
            self.enemy_turn = True

    def ObjectMenu(self):
        object_to_use = "\n"
        object_to_use = self.DrawObjectsInPocket()
        Renderer.Draw(object_to_use + "\n")
        object_to_use = input("")
        object_to_use = Check_String_Input(object_to_use, 2)
        if(object_to_use == 1):
            if(self.player.potions > 0):
                pokemon_to_heal = self.PokemonMenu()
                if(pokemon_to_heal.type != Type.Null):
                    pokemon_to_heal.heal(potion_value)
                    self.enemy_turn = True
            else:
                Renderer.Draw(Error.NoPotion.value)
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
        Renderer.Draw(text_to_print)
        action = Check_String_Input(input(""), len(self.player.pokemons))
        if(action == 0):
            if(self.red_pokemon.life_points <= 0):
                Renderer.Draw(Error.SelectedPokemonDead.value)
                return self.PokemonMenu()
            else:
                return Pokemon("None", 0, Type.Null)
        else:
            if(action > len(self.player.pokemons)):
                Renderer.Draw(Error.NotEnoughtPokemon.value)
                return self.PokemonMenu()
            elif(self.red_pokemon != self.player.pokemons[action-1]):
                if(self.player.pokemons[action-1].life_points <= 0):
                    Renderer.Draw(Error.SelectedPokemonDead.value)
                    self.enemy_turn = True
                    return self.PokemonMenu()
                    
                self.enemy_turn = True
                return self.player.pokemons[action-1]
            else:
                if(self.player.pokemons[action-1].life_points <= 0):
                    Renderer.Draw(Error.SelectedPokemonDead.value)
                    self.enemy_turn = True
                    return self.PokemonMenu()
                
                Renderer.Draw(Error.AlreadyUsePokemon.value)
                return self.red_pokemon

    def LaunchPokeball(self):
        text_to_print = ""
        if(self.action_type == Action.Wild):
            self.player.pokeball -= 1
            catch = self.TryToCatch(75, "viewp")
            time.sleep(1.0)
            if(catch):
                catch = self.TryToCatch(70, "viewp")
                time.sleep(1.0)
                if(catch):
                    catch = self.TryToCatch(60, "tic")
                    time.sleep(1.0)
                    if(catch):
                        self.player.add_pokemon(self.blue_pokemon)
                        text_to_print += PokemonInPokeballFeedback.GotIt.value
                        Renderer.Draw(text_to_print)
                        return True
                    else:
                        text_to_print += PokemonInPokeballFeedback.Try3.value
                else:
                    text_to_print += PokemonInPokeballFeedback.Try2.value
            else:
                text_to_print += PokemonInPokeballFeedback.Try1.value
                        
        elif(self.action_type == Action.Trainer):
            text_to_print += Error.PokeballOnTrainer.value

        Renderer.Draw(text_to_print)
        time.sleep(2.0)
        return False

    def Run(self, message):
        Renderer.Draw(message)
        time.sleep(1.0)

        self.red_pokemon = Pokemon("None", 0, Type.Null)
        self.blue_pokemon = Pokemon("None", 0, Type.Null)
        self.action_type = Action.Null
        self.enemy_turn = False

    def TryToCatch(self, proba, message):
        catch = random.randrange(0,100)
        if(catch < proba):
            Renderer.Draw("\n" + message + "\n")
            return True
        else:
            return False