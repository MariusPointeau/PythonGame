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

class Attack:

    def __init__(self, __name,__damages, __usage_limit, __type, __protect = False):
        self.damages = __damages
        self.usage_limit = __usage_limit
        self.usage = 0
        self.name = __name
        self.type = __type
        self.protect = __protect

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
    
    def attack(self, pokemon2):
        if self.attacks and pokemon2.life_points > 0 and not self.dead:
            has_attack = False
            attack_nb = random.randint(0, len(self.attacks)-1)
            canAttack = True
            for attack in self.attacks:
                if(attack.usage < attack.usage_limit):
                    canAttack = True
                    break
                else:
                    canAttack = False
            if not canAttack:
                pokemon2.life_points -= self.attacks[attack_nb].damages
                self.life_points -= self.attacks[attack_nb].damages
                print(self.name + " used struggle and dealt " + str(self.attacks[attack_nb].damages))
            else:
                while not has_attack:
                    if self.attacks[attack_nb].usage < self.attacks[attack_nb].usage_limit:
                        if self.attacks[attack_nb].damages > 0:
                            if pokemon2.protected:
                                print(pokemon2.name + " was protected")
                                pokemon2.protected = False
                            else:
                                pokemon2.life_points -= self.attacks[attack_nb].damages
                                print(self.name + " used " + self.attacks[attack_nb].name + " and dealt " + str(self.attacks[attack_nb].damages))
                                pokemon2.checkHP()
                        else:
                            self.protected = True
                            print(self.name + " used " + self.attacks[attack_nb].name)
                        self.attacks[attack_nb].usage += 1
                        has_attack = True
                    else:
                        attack_nb = random.randint(0, len(self.attacks)-1)

    def level_up(self, __experience):
        self.experience += __experience
        if self.experience >= 10:
            self.experience -= 10
            self.level += 1
            self.life_points += self.level
            self.maxlife_points += self.level
    
    def checkHP(self):
        if self.life_points <= 0:
            self.dead = True
            print(self.name + " is defeated")