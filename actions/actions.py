from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

from rasa_sdk.executor import CollectingDispatcher

import pandas as pd 
import numpy as np
import random 
import csv

import random 
import nltk
from nltk.corpus import names 
import unicodedata

class ActionSortUser(Action):

    def name(self) -> Text:
        return "action_sort_user"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        houses = [("gryffindor", "where dwell the brave, courageous and chivalrous at heart"), 
            ("ravenclaw", "who are know for their intelligence, wisdom and wit"), 
            ("hufflepuff", "who value hardwork, dedication, patience and loyality"),
            ("slytherin", "where roam the cunning, ambitious, resourceful people")]

        # select a random house from the houses 
        house = random.choice(houses)

        # print the house to the dispatcher 
        dispatcher.utter_message(text=f"I will sort you into {house[0]}, {house[1]}")

        return []

class ActionCastSpell(Action):

    def name(self) -> Text:
        return "action_cast_spell"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # access the file 
        spells = pd.read_csv("data/harry_potter/Spells.csv", sep=";")
        spells = spells["Incantation"].to_list()
        spells = set(spells)
        spells = list(spells)
        spells.remove("Unknown")
        spells = [x for x in spells if pd.isnull(x) == False]
        spell = random.choice(spells)

        dispatcher.utter_message(text=f"*Flicks wand dramatically* \r{spell} \rWhoosh!!!!")

        return []



class ActionIsCharacter(Action):

    def name(self) -> Text:
        return "action_is_character" # specify in domain.yml file as well 

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # access the file 
        # filter and store the data in a list
        chrctrs = pd.read_csv("data/harry_potter/Characters.csv", sep=";")
        chrctrs = chrctrs["Name"].to_list() 
        chrctrs = set(chrctrs)
        chrctrs = [x.lower() for x in chrctrs if pd.isnull(x) == False]
        # get list of first and last names 
        fl_names = []
        for chrctr in chrctrs:
            name = chrctr.split(" ")
            if len(name) == 3:
                fl = name[0] + " " + name[2] 
                fl_names.append(fl)

        # get list of first names only 
        f_names = []
        for chrctr in chrctrs:
            f_name = chrctr.split(" ")
            f_names.append(f_name[0])

        for blob in tracker.latest_message["entities"]:
            if blob["entity"] == "character_type":
                character = blob["value"]
                if character in chrctrs:
                    dispatcher.utter_message(text=f"yes, {character} is a Harry Potter character")
                elif character in fl_names:
                    dispatcher.utter_message(text=f"yes, {character} is a Harry Potter character")
                elif character in f_names:
                    dispatcher.utter_message(text=f"yes, {character} is a Harry Potter character")
                else:
                    dispatcher.utter_message(text=f"sorry {character} is not a Harry Potter character")
                
                

        return []

class ActionCastSpell(Action):

    def name(self) -> Text:
        return "action_cast_spell"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # access the file 
        spells = pd.read_csv("data/harry_potter/Spells.csv", sep=";")
        spells = spells["Incantation"].to_list()
        spells = set(spells)
        spells = list(spells)
        spells.remove("Unknown")
        spells = [x for x in spells if pd.isnull(x) == False]
        spell = random.choice(spells)

        dispatcher.utter_message(text=f"Flicks wand dramatically {spell} Whoosh!!!!")

        return []



class ActionPotionEffect(Action):

    def name(self) -> Text:
        return "action_potion_effect"  

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # access the file 
        # filter and store the data in a list
        potions = pd.read_csv("data/harry_potter/Potions.csv", sep=";")

        for blob in tracker.latest_message["entities"]:
            if blob["entity"] == "potion_type":
                potion = blob["value"].capitalize()
                # check if the potion exists in the file 
                if potion in set(potions["Name"]):
                    potion_ef = potions.loc[potions["Name"] == potion]
                    ef = potion_ef["Effect"].to_list()
                    ef = unicodedata.normalize("NFKD", ef[0])
                    dispatcher.utter_message(text=f"{ef}")
                else:
                    dispatcher.utter_message(text=f"Sorry I don't know information about this potion :(")


        return []

class ActionPotionIngredients(Action):

    def name(self) -> Text:
        return "action_potion_ingredients"  

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # access the file 
        # filter and store the data in a list
        potions = pd.read_csv("data/harry_potter/Potions.csv", sep=";")

        for blob in tracker.latest_message["entities"]:
            if blob["entity"] == "potion_type":
                potion = blob["value"].capitalize()
                # check if the potion exists in the file 
                if potion in set(potions["Name"]):
                    potion_ing = potions.loc[potions["Name"] == potion]
                    ingredients = potion_ing["Known ingredients"].to_list()
                    if  np.isnan(ingredients):
                        dispatcher.utter_message(text=f"Sorry I don't know how this potion is made :(")
                    else:
                        ingredients = unicodedata.normalize("NFKD", ingredients[0])
                        dispatcher.utter_message(text=f"{ingredients}")
                else:
                    dispatcher.utter_message(text=f"Sorry I don't know information about this potion :( Are you sure its a real potion?")


        return []


class ActionGreetName(Action):

    def name(self) -> Text:
        return "action_greet_name"
    
    def run(self,
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        # get the word from the entity 
        for blob in tracker.latest_message["entities"]:
            if blob["entity"] == "user_name":
                name = blob["value"]
                dispatcher.utter_message(text=f"Hey {name}. Nice to meet you!")
        return []