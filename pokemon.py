import random
from enum import Enum

class Type(Enum):
    Fire = "1"
    Water = "2"
    Grass = "3"
    Flying = "4"
    Dragon = "5"
    Psy = "6"
    Electric = "7"
    Rock = "8"
    Normal = "9"
    Buff = "10"
    Null = "11"

    @classmethod
    def Adventage(cls, type1, type2) -> float:
        if(type1 == Type.Fire and type2 == Type.Grass):
            return 1.5
        elif(type1 == Type.Water and (type2 == Type.Fire or type2 == Type.Rock)):
            return 1.5
        elif(type1 == Type.Grass and type2 == Type.Water):
            return 1.5
        elif(type1 == Type.Flying and type2 == Type.Grass):
            return 1.5
        elif(type1 == Type.Dragon and type2 == Type.Normal):
            return 1.5
        elif(type1 == Type.Psy and type2 == Type.Dragon):
            return 1.5
        elif(type1 == Type.Electric and (type2 == Type.Water or type2 == Type.Flying)):
            return 1.5
        elif(type1 == Type.Rock and (type2 == Type.Psy or type2 == Type.Electric)):
            return 1.5
        
        if(type1 == Type.Fire and type2 == Type.Water):
            return 0.5
        elif(type1 == Type.Water and (type2 == Type.Grass or type2 == Type.Electric)):
            return 0.5
        elif(type1 == Type.Grass and (type2 == Type.Fire or type2 == Type.Flying)):
            return 0.5
        elif(type1 == Type.Flying and type2 == Type.Electric):
            return 0.5
        elif(type1 == Type.Dragon and type2 == Type.Psy):
            return 0.5
        elif(type1 == Type.Psy and type2 == Type.Rock):
            return 0.5
        elif(type1 == Type.Electric and type2 == Type.Rock):
            return 0.5
        elif(type1 == Type.Rock and type2 == Type.Water):
            return 0.5
        elif(type1 == Type.Normal and type2 == Type.Dragon):
            return 0.5
        return 1

class Attack:

    def __init__(self, __name,__damages, __usage_limit, __type, __protect = False):
        self.damages = __damages
        self.usage_limit = __usage_limit
        self.usage = 0
        self.name = __name
        self.type = __type
        self.protect = __protect
    
    def copy(self):
        attack_copy = Attack(self.name,self.damages,self.usage_limit,self.type,self.protect)
        return attack_copy

class Pokemon:
    counter = 0
    
    def __init__(self, __name, __life_points, __type):
        self.name = __name
        self.experience = 0
        self.level = 1
        self.life_points = __life_points * self.level
        self.maxlife_points = self.life_points
        self.dead = False
        self.protected = False
        self.attacks = []
        self.type = __type
        Pokemon.counter += 1
        
    def __str__(self):
         return self.name + " " + str(self.life_points) + " " + str(len(self.attacks))
        
    def add_attack(self, attack):
        if len(self.attacks) < 4:
            if not attack in self.attacks:
                self.attacks.append(attack)
    
    def heal(self, hp_restored):
        self.life_points += hp_restored
        for attack in self.attacks:
            attack.usage -= hp_restored
            if attack.usage < 0:
                attack.usage = 0
    
    def attack(self, attack: Attack, pokemon2):
        attack_message = "\n"
        if self.attacks and pokemon2.life_points > 0 and not self.dead:
            canAttack = True
            if(attack.usage < attack.usage_limit):
                canAttack = True
            else:
                canAttack = False
            if not canAttack:
                pokemon2.life_points -= attack.damages
                self.life_points -= attack.damages
                attack_message += self.name + " used struggle and dealt " + str(attack.damages)
                attack_message += pokemon2.checkHP()
                attack_message += self.checkHP()
            else:
                if attack.damages > 0:
                    if pokemon2.protected:
                        attack_message += pokemon2.name + " was protected"
                        pokemon2.protected = False
                    else:
                        pokemon2.life_points -= int(attack.damages * Type.Adventage(attack.type, pokemon2.type))
                        attack_message += self.name + " used " + attack.name + " and dealt " + str(int(attack.damages * Type.Adventage(attack.type, pokemon2.type)))
                        attack_message += pokemon2.checkHP()
                else:
                    self.protected = True
                    attack_message += self.name + " used " + attack.name
                attack.usage += 1
        return attack_message + "\n"

    def level_up(self, __experience):
        self.experience += __experience
        if self.experience >= 10:
            self.experience -= 10
            self.level += 1
            self.life_points += self.level
            self.maxlife_points += self.level

            return self.name + " leveled up\n" + "\n he's now level " + str(self.level)
        return ""
    
    def checkHP(self):
        if self.life_points <= 0:
            self.dead = True
            self.life_points = 0
            return "\n\n" + self.name + " is defeated"
        else:
            return ""
        
    def copy(self):
        pokemon_copy = Pokemon(self.name, self.life_points, self.type)
        pokemon_copy.attacks = self.attacks
        return pokemon_copy
    
    def GetRandomAttack(self):
        attack : Attack = random.choice(self.attacks)
        if(attack.usage < attack.usage_limit):
            for list_attack in self.attacks:
                if(list_attack.usage < list_attack.usage_limit):
                    attack = list_attack
                    break
        return attack