import cards
import random

class Deck:
    def __init__(self):
        self.cards = cards.initialyze()

    def get_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
