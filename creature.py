import player
import ability

class Creature:
    def __init__(self, owner, card, id):
        self.card = card
        self.id = id
        self.hunger = 1
        self.food = 0
        self.fat = 0
        self.abilities = []
        serf.owner = owner
        #print("{} has spawned a new creature (ID: {})".format(self.owner, self.id))

    def __init__(self, json):
        self.id == json["id"]
        self.hunger = json["hunger"]
        self.food = json["food"]
        self.fat = json["fat"]
        self.abilities = []
        for ability in json["abilities"]:
            self.abilities.append(ability)
        serf.owner = json["owner"]

    def add_ability(self, card):
        self.abilities.append(card)

    def json(self):
        json = {}
        json["id"] = self.id
        json["hunger"] = self.hunger
        json["food"] = self.food
        json["fat"] = self.fat
        json["owner"] = self.owner
        json["abilities"] = {}
        for ability in self.abilities:
            json["abilities"].append(ability)
        json["card"] = card.id
        return json
