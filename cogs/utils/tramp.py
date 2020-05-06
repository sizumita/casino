import random
import pathlib
suits = ['c', 'd', 'h', 's']
ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def path(self):
        return str(pathlib.Path.cwd()/'images'/f'{self.suit}{self.rank}.png')

class Joker(Card):
    def __init__(self):
        super().__init__(0, 0)

    def path(self):
        return pathlib.Path.cwd()/'images'/f'joker.png'

class Deck:
    def __init__(self, joker_count=0):
        self.cards = [Card(suit, rank) for rank in ranks for suit in suits]
        self.cards += [Joker() for i in range(joker_count)]

        self.joker_count = joker_count

        self.drawed = []

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        card = self.cards.pop(0)
        self.drawed.append(card)

        return card

    def next(self) -> Card:
        return self.cards[0]

    def reset(self):
        self.cards = [Card(suit, rank) for rank in ranks for suit in suits]
        self.cards += [Joker() for i in range(self.joker_count)]

    def take_back(self):
        """最後に引いたやつを戻す"""
        self.cards = [self.drawed.pop(-1)] + self.cards
