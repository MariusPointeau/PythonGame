from dresseur import *
from map import *

red = Dresseur("Red", 0, 1)

blue = Dresseur("Blue", 0, 1)

p1 = Pokemon("Pikachu", random.randint(80,120))
Vive_Attaque = Attack("Vive_Attaque", 5, 25)
p1.add_attack(Vive_Attaque)
Charme = Attack("Charme", 0, 25)
p1.add_attack(Charme)
Tonnerre = Attack("Tonnerre", 20, 15)
p1.add_attack(Tonnerre)
Fatal_Foudre = Attack("Fatal_Foudre", 80, 5)
p1.add_attack(Fatal_Foudre)
red.add_pokemon(p1)

p1 = Pokemon("Mentali", random.randint(80,120))
Météores = Attack("Météores", 20, 10)
p1.add_attack(Météores)
Protection = Attack("Protection", 0, 5, True)
p1.add_attack(Protection)
Coud_Boue = Attack("Coud'Boue", 5, 25)
p1.add_attack(Coud_Boue)
Psyko = Attack("Psyko", 50, 10)
p1.add_attack(Psyko)
red.add_pokemon(p1)

p1 = Pokemon("Ronflex", random.randint(80,120))
Plaquage = Attack("Plaquage", 40, 15)
p1.add_attack(Plaquage)
Repos = Attack("Repos", 0, 5, True)
p1.add_attack(Repos)
Ronflement = Attack("Ronflement", 20, 15)
p1.add_attack(Ronflement)
Amnesie = Attack("Amnesie", 75, 5)
p1.add_attack(Amnesie)
red.add_pokemon(p1)

p1 = Pokemon("Florizarre", random.randint(80,120))
Giga_Sangsue = Attack("Giga_Sangsue", 70, 10)
p1.add_attack(Giga_Sangsue)
Zenith = Attack("Zenith", 5, 25)
p1.add_attack(Zenith)
Synthese = Attack("Synthese", 5, 15)
p1.add_attack(Synthese)
Lance_Soleil = Attack("Lance_Soleil", 65, 10)
p1.add_attack(Lance_Soleil)
red.add_pokemon(p1)

p1 = Pokemon("Dracaufeu", random.randint(80,120))
Cru_Aile = Attack("Cru_Aile", 5, 25)
p1.add_attack(Cru_Aile)
Danseflamme = Attack("Danseflamme", 0, 25)
p1.add_attack(Danseflamme)
Tranche = Attack("Tranche", 20, 15)
p1.add_attack(Tranche)
Lance_Flamme = Attack("Lance-Flamme", 45, 10)
p1.add_attack(Lance_Flamme)
red.add_pokemon(p1)

p1 = Pokemon("Tortank", random.randint(80,120))
Surf = Attack("Surf", 35, 20)
p1.add_attack(Surf)
Danse_Pluie = Attack("Danse Pluie", 0, 5, True)
p1.add_attack(Danse_Pluie)
Blizzard = Attack("Blizzard", 15, 20)
p1.add_attack(Blizzard)
Siphon = Attack("Siphon", 10, 20)
p1.add_attack(Siphon)
red.add_pokemon(p1)

#////////////////////////////////////////////////////////////////////////BLUE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

p1 = Pokemon("Roucarnage", random.randint(80,120))
p1.add_attack(Vive_Attaque)
Cyclone = Attack("Cyclone", 20, 15)
p1.add_attack(Cyclone)
p1.add_attack(Cru_Aile)
Mimique = Attack("Mimique", 5, 25)
p1.add_attack(Mimique)
blue.add_pokemon(p1)

p1 = Pokemon("Noadkoko", random.randint(80,120))
p1.add_attack(Zenith)
p1.add_attack(Giga_Sangsue)
BombOeuf = Attack("BombOeuf", 15, 25)
p1.add_attack(BombOeuf)
p1.add_attack(Lance_Soleil)
blue.add_pokemon(p1)

p1 = Pokemon("Arcanin", random.randint(80,120))
Hurlement = Attack("Hurlement", 10, 15)
p1.add_attack(Hurlement)
p1.add_attack(Météores)
p1.add_attack(Lance_Flamme)
Vit_Ext = Attack("Vit_Ext", 75, 5)
p1.add_attack(Vit_Ext)
blue.add_pokemon(p1)

p1 = Pokemon("Léviator", random.randint(80,120))
Ouragan = Attack("Ouragan", 70, 10)
p1.add_attack(Ouragan)
Hydrocanon = Attack("Hydrocanon", 65, 10)
p1.add_attack(Hydrocanon)
p1.add_attack(Danse_Pluie)
Ultralaser = Attack("Ultralaser", 100, 5)
p1.add_attack(Ultralaser)
blue.add_pokemon(p1)

p1 = Pokemon("Rhinoferos", random.randint(80,120))
Furie = Attack("Furie", 15, 15)
p1.add_attack(Furie)
Tempetesable = Attack("Tempetesable", 5, 25)
p1.add_attack(Tempetesable)
Eboulement = Attack("Eboulement", 20, 15)
p1.add_attack(Eboulement)
Seisme = Attack("Seisme", 45, 10)
p1.add_attack(Seisme)
blue.add_pokemon(p1)

p1 = Pokemon("Alakazam", random.randint(80,120))
Entrave = Attack("Entrave", 35, 20)
p1.add_attack(Entrave)
Soin = Attack("Soin", 0, 5, True)
p1.add_attack(Soin)
p1.add_attack(Psyko)
p1.add_attack(Protection)
blue.add_pokemon(p1)

map = Map()

print(map)