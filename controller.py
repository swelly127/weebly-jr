import random
import math

RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
SUITS = ('Spades', 'Diamonds', 'Hearts', 'Clubs')

TRANSLATE =    {2: "2", 3: "3", 4: "4", 5: "5", 
                6: "6", 7: "7", 8: "8", 9: "9",
                10: "10", 11: 'Jack', 12: 'Queen', 
                13: 'King', 14: 'Ace'}

SMALL_BLIND = 5
LARGE_BLIND = SMALL_BLIND * 2

class Card:

    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def __str__(self):
        return TRANSLATE[self._rank] + " of " + self._suit

    def __lt__(self, other):
        return self._rank < other.get_rank()


class Deck:

    _cards = []

    def __init__(self):
        for s in SUITS:
            for r in RANKS:
                self._cards.append(Card(r, s))


    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self):
        if len(self._cards) == 0:
            return None
        else:
            return self._cards.pop()

    def __len__(self):
        return len(self._cards)

    def __str__(self):
        result = ""
        for c in self._cards:
            result = result + str(c) + '\n'
        return result

class Game:

    _deck = Deck()
    _players = []
    _pot = 0

    _table_cards = []

    def __init__(self):
        p1_cards = [self._deck.deal(), self._deck.deal()]
        p2_cards = [self._deck.deal(), self._deck.deal()]
        _players = [Player(p1_cards), Player(p2_cards)]

    def deal(self):
        if self._table_cards == []:
            self._table_cards = [self._deck.deal(), self._deck.deal(), self._deck.deal()]
        else:
            self._table_cards.append(self._deck.deal())

    def prompt_player(self):
        pass

    def award_pot(self, winner):
        winner.chips = winner.chips + self._pot

class Player:

    chips = 100
    name = ""
    move_history = []

    _cards = []

    _hand = []
    _myranks = [0] * 14
    _mysuits = [0] * 4

    def __init__(self, cards):
        self._cards = cards
        self._cards.sort(reverse=True)

    def __str__(self):
        result = ""
        for card in self._cards:
            result = result +str(card)+ '\n'
        return result

    # return -1 -> fold
    # return 0 -> call or check
    # return x > 0 -> raise by x
    def move(self, game):
        table_score = evaluateHand(game.table_cards)
        my_score = evaluateHand(self._cards + table_cards)
        if my_score < table_score + 100:
            return 0
        else: 
            return 25

    def evaluateHand(self, cards):
        self._hand = cards;
        self._hand.sort(reverse=True)
        self._myranks = [0] * 14
        self._mysuits = [0] * 4
        for card in self._hand:
            rankIndex = RANKS.index(card.getRank())
            suitIndex = SUITS.index(card.getSuit())
            self._myranks[rankIndex] += 1
            self._mysuits[suitIndex] += 1
        return score()

    def hasFlush(self):
        return 5 in self.mysuits

    def hasFourOfAKind(self):
        return 4 in self.myranks

    def hasFullHouse(self):
        return self._myranks.count(3) == 2 or (self.hasPair() and self.hasThreeOfAKind())

    def hasThreeOfAKind(self):
        return 3 in self.myranks

    def hasTwoPair(self):
        return self._myranks.count(2) == 2

    def hasPair(self):
        return 2 in self.myranks

    def hasRoyalStraight(self):
        return (    self._myranks[10] == 1
                    and self._myranks[11] == 1
                    and self._myranks[12] == 1
                    and self._myranks[13] == 1
                    and self._myranks[14] == 1 )

    def hasStraight(self):
        for i in range(10):
            if ( self._myranks[i]   == 1 and
                 self._myranks[i+1] == 1 and
                 self._myranks[i+2] == 1 and
                 self._myranks[i+3] == 1 and
                 self._myranks[i+4] == 1 ):
                return True
        return False

    def hasStraightFlush(self):
        return self.hasStraight() and self.hasFlush()

    def hasRoyalFlush(self):
        return self.hasRoyalStraight() and self.hasFlush()

    def score(self):
        if self.hasRoyalFlush():
            return 90
        elif self.hasStraightFlush():
            return 80
        elif self.hasFourOfAKind():
            return 70
        elif self.hasFullHouse():
            return 60
        elif self.hasFlush():
            return 50
        elif self.hasStraight():
            return 40
        elif self.hasThreeOfAKind():
            return 30
        elif self.hasTwoPair():
            return 20
        elif self.hasPair():
            return 10
        else:
            return 0

    def printHand(self):
        if self.hasRoyalFlush():
            return "Royal Flush"
        elif self.hasStraightFlush():
            return "Straight Flush"
        elif self.hasFourOfAKind():
            return "Four of a Kind"
        elif self.hasFullHouse():
            return "Full House"
        elif self.hasFlush():
            return "Flush"
        elif self.hasStraight():
            return "Straight"
        elif self.hasThreeOfAKind():
            return "Three of A Kind"
        elif self.hasTwoPair():
            return "Two pair"
        elif self.hasPair():
            return "Pair"
        else:
            return "High Card " + str(self._hand[0])
