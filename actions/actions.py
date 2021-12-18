# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from random import randint
import csv
import os.path


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


class ActionSaveOrder(Action):

    def name(self) -> Text:
        return 'action_save_order'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get slots values
        food = str(tracker.get_slot('food'))
        time = str(tracker.get_slot('time'))
        # create a random order ID
        order_id = f'AA{random_with_N_digits(5)}'

        # check if orders file exists
        filename = './files/orders.csv'

        if os.path.exists(filename):
            # append if already exists
            file = open(filename, 'a', newline='')
        else:
            # make a new file if not
            file = open(filename, 'w', newline='')
            writer = csv.writer(file)
            writer.writerow(['Order ID', 'Time', 'Plate'])

        writer = csv.writer(file)
        writer.writerow([order_id, time, food])
        file.close()
        dispatcher.utter_message(text=f'Order Saved! Your order ID is {order_id}')

        return []

    
