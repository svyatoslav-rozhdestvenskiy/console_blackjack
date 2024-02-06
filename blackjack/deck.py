from card_for_print import Card
from random import shuffle


class CardDeck:
    def __init__(self):
        self.card_count = 0
        self.deck = []
        self.new_deck_creator()

    def new_deck_creator(self):
        suits = Card.suits.keys()
        ranks = Card.card_values.keys()
        deck_base = []
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                deck_base.append(card)
        shuffle(deck_base)
        self.deck = deck_base
        self.card_count = len(self.deck)

    def get_deck(self):
        return self.deck

    def pop_deck(self, element=0):
        self.deck.pop(element)

    def get_card_count(self):
        return self.card_count

    def set_card_count(self):
        self.card_count = len(self.deck)
