from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

from rasa_sdk.executor import CollectingDispatcher

import pandas as pd 
import random 
import csv

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