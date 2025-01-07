class Tile:

    def __init__(self):
        self.occupied = False
        self.player = False
        self.potion = False
    
    def tileForm(self):
        if(self.occupied):
            if(self.player):
                return "|^_^|"
            elif(self.potion):
                return "| * |"
        return "|   |"

class Map:
    tiles = []

    def __init__(self):
        for i in range(0,26):
            tile = Tile()
            if(i == 13):
                tile.occupied = True
                tile.player = True
            self.tiles.append(tile)
    
    def __str__(self):
        textToPrint = "-------------------------" + "\n"
        for i in range(1,26):
            textToPrint += self.tiles[i].tileForm()
            if(i % 5 == 0 and not i == 0):
                textToPrint += "\n" + "-------------------------" + "\n"
        return textToPrint
