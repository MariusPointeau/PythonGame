from dresseur import *
from map import *

class Game:
    map = Map()
    pokemons = []
    playerPos = 13

    close = False

    def __init__(self, __pokemons, __map):
        self.pokemons = __pokemons
        self.map = __map
    
    def DrawMap(self):
        print(self.map)
    
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
    
    def PlayerMoved(self, howMuch):
        self.map.tiles[self.playerPos].occupied = False
        self.map.tiles[self.playerPos].player = False
        self.playerPos += howMuch
        self.map.tiles[self.playerPos].occupied = True
        self.map.tiles[self.playerPos].player = True

    def Update(self):
        self.DrawMap()
        self.GetKey()
        print("\033c")