from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

from rasa_sdk.executor import CollectingDispatcher

import pandas as pd 
import random 
import csv

import random 
import nltk
from nltk.corpus import names 

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

        dispatcher.utter_message(text=spell)

        return []

class ActionGreetName(Action):

    labeled_names = ([(name, "male") for name in names.words("male.txt")] + 
                     [(name, "female") for name in names.words("female.txt")])

    random.shuffle(labeled_names)
    features = [({"last_letter": lambda n: n[-5:]}, gender) for (n, gender) in labeled_names]

    train_set, test_set = features[:500], features[500:]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    def name(self) -> Text:
        return "action_greet_name"

    # # helper function 
    # def gender_features(word):
    #     return {"last_letter": word[-1]}
    
    def run(self,
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        # get the word from the entity 
        for blob in tracker.latest_message["entities"]:
            if blob["entity"] == "user_name":
                name = blob["value"]
                result = self.classifier.classify({"last_letter": name[-5:]})
                if result == "female":
                    dispatcher.utter_message(text=f"Hi {name}. Yer a witch, {name}")
                elif result == "male":
                    dispatcher.utter_message(text=f"Hi {name}. Yer a wizard, {name}")
        return []