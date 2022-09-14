import os
import json

class Deck:
    def __init__(self):
        self.name = 'My Deck'
        self.format = 'Standard'
        self.isValid = False
        self.tags = []
        self.cards = []

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def create_file(self, file_path):
        json_file = json.loads(self.get_json())
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

class CardInDeck:
    def __init__(self):
        self.id = ''
        self.board = 1
        self.quantity = 0

def create_default_deck():
    if len(os.listdir('./decks')) <= 0:
        collection = Deck()
        collection.cards.append(CardInDeck())
        collection.create_file(f"./decks/{collection.name}.json")

create_default_deck()