import creature
import ability

class Player:
    def __init__(self, mode, **kwargs):
        if (mode == 'init'):
            self.name = kwargs["name"]
            deck = kwargs["deck"]
            self.creatures = []
            self.cards = []
            self.creature_index = 0
            self.finished = "false"
            self.discard = 0
            for index in range(0, 5):
                self.cards.append(deck.get_card())
        elif (mode == 'load'):
            json = kwargs["json"]
            self.name = json["name"]
            self.finished = json["finished"]
            self.discard = json["discard"]
            self.creature_index = json["creature_index"]
            self.cards = []
            self.creatures = []
            for card in json["cards"]:
                self.cards.append(card)
            for creature in json["creatures"]:
                self.creatures.append(Creature(creature))


    def add_creature(self, card):
        creature = Creature(self.name, card, self.creature_index)
        self.creatures.append(creature)
        self.creature_index = self.creature_index + 1

    def json(self):
        json = {}
        json["name"] = self.name
        json["creatures"] = {}
        json["finished"] = self.finished
        json["creature_index"] = self.creature_index
        for creature in self.creatures:
            json["creatures"][creature.id] = creature.json()
        json["cards"] = []
        for card in self.cards:
            json["cards"].append(card)
        json["discard"] = self.discard
        return json
