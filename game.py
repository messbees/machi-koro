import creature
import player
import deck
import ability
import random
import json
from player import Player
#from exceptions import EvolutionServerException

class Game:
    def __init__(self, mode, **kwargs): #name, players, deck):
        if (mode == 'init'):
            name = kwargs["name"]
            players = kwargs["players"]
            deck = kwargs["deck"]
            self.name = name
            self.id = random.randrange(1000, 9999)
            self.round = 1
            self.stage = "evolution"
            first = random.choice(players)
            self.turn = first.name
            self.players = players
            for index in (0, len(self.players)-2):
                players[index].next = players[index+1]
            players[len(self.players)-1].next = first
            self.dice = 0
            self.food = 0
            self.deck = deck
        elif (mode == 'load'):
            json = kwargs["json"]
            self.name = json["name"]
            self.id = json["id"]
            self.round = json["round"]
            self.stage = json["stage"]
            self.turn = json["turn"]
            self.players = []
            self.dice = 0
            self.food = 0
            self.deck = json["deck"]
            for player in json["players"]:
                self.players.append(Player('load', json=player))

    def do_evolution(self, player, creature, card):
        if not (self.turn == player.name):
            return false

        for p in self.players:
            if (p == player):
                player = p
        else:
            return false

        if (creature == 999):
            player.add_creature(card)

        else:
            cc = None
            for c in player.creatures:
                if (c.id == creature):
                    c.add_ability(card)
                    cc = c
                    print('Creature {} of {} now have ability"{}" from {}.'.format(c.id, player.name, card, player.name))
            if (cc == None):
                return false

        if (creature == 0 and player.finished == "false"):
            player.finished = "true"


        for p in self.players:
            if (p.finished == "false"):
                return true

        self.stage = "survival"
        self.turn = first.name

    def save(self):
        game = self.json()
        with open('games/{}.json'.format(self.id), 'w') as outfile:
            json.dump(game, outfile)

    def json(self):
        json = {}
        json["name"] = self.name
        json["id"] = self.id
        json["round"] = self.round
        json["stage"] = self.stage
        json["turn"] = self.turn
        json["dice"] = self.dice
        json["food"] = self.food
        json["players"] = []
        for player in self.players:
            json["players"].append(player.json())
        json["deck"] = []
        #print(self.deck)
        for card in self.deck:
            json["deck"].append(card)
        return json
