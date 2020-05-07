import random
import pathlib
suits = ['c', 'd', 'h', 's']
ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
emoji_id_dict = {
    'c1': 707840091116011580,
    'd1': 707840092575760514,
    'h1': 707840093917937756,
    's1': 707840095788466187,
    'c2': 707840097143226448,
    'd2': 707840099965993040,
    'h2': 707840101551439914,
    's2': 707840103086555178,
    'c3': 707840104793899018,
    'd3': 707840106312105984,
    'h3': 707840107826380830,
    's3': 707840110174928926,
    'c4': 707840114877005835,
    'd4': 707840116265320479,
    'h4': 707840117796241439,
    's4': 707840119339483198,
    'c5': 707840121382240277,
    'd5': 707840122816823348,
    'h5': 707840124573974528,
    's5': 707840125731602443,
    'c6': 707840127195676683,
    'd6': 707840128386859039,
    'h6': 707840130081357826,
    's6': 707840131331129396,
    'c7': 707840132807524354,
    'd7': 707840134711607346,
    'h7': 707840136062173254,
    's7': 707840138809573409,
    'c8': 707840140999131166,
    'd8': 707840142316142693,
    'h8': 707840143738011729,
    's8': 707840145050566668,
    'c9': 707840146732482623,
    'd9': 707840148523581460,
    'h9': 707840149647786095,
    's9': 707840151300341861,
    'c10': 707840152713560084,
    'd10': 707840153791758387,
    'h10': 707840155314290700,
    's10': 707840157403054080,
    'c11': 707840160888520785,
    'd11': 707840163417686036,
    'h11': 707840166148046868,
    's11': 707840169197305856,
    'c12': 707840173362249728,
    'd12': 707840176210051132,
    'h12': 707840178802130965,
    's12': 707840181822160926,
    'c13': 707840185538183188,
    'd13': 707840190080745523,
    'h13': 707841597999677451,
    's13': 707841652177502269,
    'joker': 707841679729754113,
}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.name = f'{suit}{rank}'

    def path(self):
        return str(pathlib.Path.cwd()/'images'/f'{self.suit}{self.rank}.png')

    def emoji_id(self):
        return emoji_id_dict[self.name]


class Joker(Card):
    def __init__(self):
        super().__init__(0, 0)
        self.name = 'joker'

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
