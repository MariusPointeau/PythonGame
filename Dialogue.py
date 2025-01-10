from enum import Enum
from Engine import Renderer
import random
import time

class Trainer_Dialogue(Enum):
    Greatings = "\nHello Trainer I'm "
    AskName = "\nWhat's your name ?\n"
    Nice = "\nNice to meet you "
    NoticePokemon = "\nI noticed you have pokemons in your pocket "
    Challenge = ". Do you want to challenge me to a pokemon battle ?\n"

    Accepted = "\nLet's go !\n"
    Declined = "\nToo sad\n"

    DifferentName = "\nYou didn't say that name to my trainer friend. Your name is "
    Didnt_understand = "\nI didn't understand your answer, I'll repeat for you\n"
    Insult_response = "\nIs that so ?"

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def CheckInList(cls, str : str) -> bool:
        check = str.split(" ")
        for i in check:
            if(i in cls.list()):
                return True
        return False

class PositiveResponse(ExtendedEnum):
    first = "yes"
    second = "yeah"
    third = "of course"
    forth = "i do"
    fifth = "yeap"

class NegativeResponse(ExtendedEnum):
    first = "no"
    second = "nope"
    third = "don't"
    forth = "do not"
    fifth = "never"

class Insults(ExtendedEnum):
    disgusted = "disgusted"
    chicken = "chicken"
    hate = "hate"
    donkey = "donkey"
    nerd = "nerd"
    pig = "pig"


class Dialogue:
    player_name = ""

    def __init__(self, __interaction_name, __nb_pokemon):
        self.interaction_name = __interaction_name
        self.nb_pokemon = __nb_pokemon
    
    def Conversation(self) -> bool:
        self.StartConversation()
        return self.ChallengePlayer()
    
    def StartConversation(self):
        text_to_print = Trainer_Dialogue.Greatings.value + self.interaction_name + Trainer_Dialogue.AskName.value
        Renderer.Draw(text_to_print)
        response = input("")
        if(response != Dialogue.player_name and Dialogue.player_name is not ""):
            text_to_print = Trainer_Dialogue.DifferentName.value + Dialogue.player_name + " if I remember correctly\n"
        else:
            Dialogue.player_name = response
            text_to_print = Trainer_Dialogue.Nice.value + Dialogue.player_name
        Renderer.Draw(text_to_print)

        time.sleep(1.0)
    
    def ChallengePlayer(self):
        text_to_print = Trainer_Dialogue.NoticePokemon.value + Dialogue.player_name + Trainer_Dialogue.Challenge.value
        Renderer.Draw(text_to_print)
        response = input("")
        response = response.lower()
        if(Insults.CheckInList(response)):
            Renderer.Draw(Trainer_Dialogue.Insult_response.value)
            return True
        elif(PositiveResponse.CheckInList(response)):
            Renderer.Draw(Trainer_Dialogue.Accepted.value)
            return True
        elif(NegativeResponse.CheckInList(response)):
            Renderer.Draw(Trainer_Dialogue.Declined.value)
            return False
        else:
            Renderer.Draw(Trainer_Dialogue.Didnt_understand.value)
            return self.ChallengePlayer()



    def InformationGathering(self):
        pass
    