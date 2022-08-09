import collections
import os
import json

class Collection:
    def __init__(self):
        self.name = 'Collection'
        self.cards = []

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def create_file(self, file_path):
        json_file = json.loads(self.get_json())
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

class CardInCollection:
    def __init__(self):
        self.id = ''
        self.regular = 0
        self.foil = 0
        self.tags = []

def create_default_collection():
    if len(os.listdir('./collections')) <= 0:
        collection = Collection()
        collection.cards.append(CardInCollection())
        collection.create_file(f"./collections/{collection.name}.json")

create_default_collection()