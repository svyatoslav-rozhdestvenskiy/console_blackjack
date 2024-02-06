class Card:
    card_values = {
        'Ace': 11,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10
    }
    suits = {
        'Spades': '♠',
        'Diamonds': '♦',
        'Hearts': '♥',
        'Clubs': '♣',
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.points = self.card_values[rank]


def join_card(cards_to_join):
    card_split = list(card.splitlines() for card in cards_to_join)
    return '\n'.join(' '.join(string) for string in zip(*card_split))


def ascii_version_of_card(*cards):
    if isinstance(cards[0], list):
        cards = tuple(cards[0])
    card_model = """\
┌─────────┐
│{}       │
│         │
│         │
│    {}   │
│         │
│         │
│       {}│
└─────────┘
""".format('{rank: <2}', '{suit: <2}', '{rank: >2}')

    def card_format(card):
        rank = card.rank if card.rank == '10' else card.rank[0]
        suit = card.suits[card.suit]
        return card_model.format(rank=rank, suit=suit)
    return join_card(map(card_format, cards))


def ascii_version_of_hidden_card(*cards):
    if isinstance(cards[0], list):
        cards = tuple(cards[0])
    hidden_card_model = """\
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘
"""
    return join_card((hidden_card_model, ascii_version_of_card(*cards[1::])))
