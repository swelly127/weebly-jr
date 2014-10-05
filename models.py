#!/usr/bin/env python
import os
import json
import requests
import datetime
import settings
import random
import math
import pytz
from settings import *
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', POSTGRES_DB)
db = SQLAlchemy(app)

RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
SUITS = ('Spades', 'Diamonds', 'Hearts', 'Clubs')

TRANSLATE = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}

class Card:
  def __init__(self, rank, suit):
    self._rank = rank
    self._suit = suit
  def get_rank(self):
    return self._rank
  def get_suit(self):
    return self._suit
  def image_name(self):
    return str(self._rank) + str(self._suit) + ".png"
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

class Hand:
  _myranks = [0] * 14
  _mysuits = [0] * 4
  _cards = []

  def __init__(self, cards):
    self._cards = cards
    self._cards.sort(reverse=True)

    for card in self._cards:
      rankIndex = RANKS.index(card.getRank())
      suitIndex = SUITS.index(card.getSuit())
      self._myranks[rankIndex] += 1
      self._mysuits[suitIndex] += 1

  def __str__(self):
    result = ""
    for card in self._cards:
      result = result +str(card)+ '\n'
    return result

  def numCards(self):
    return len(self._cards)

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
    return ( self._myranks[10] == 1
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

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.String(80), primary_key=True)
    aggressiveness = db.Column(db.Integer) # num between -100 and 100 from safe to frequent raiser
    metadata = db.Column(JSON)
    access_token = db.Column(db.String(80), unique=True)
    small_blind = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    chips = db.Column(db.Integer)
    joined = db.Column(db.DateTime)

    def __init__(self, _id):
      self.id = _id
      self.aggressiveness = 0
      self.balance = 0
      self.joined = datetime.now()

    @property
    def balance(self):
      return (self.chips)/100.0

    @property
    def serialize(self):
      return {
        'id': self.id,
        'metadata': self.metadata,
        'access_token': self.access_token,
        'email': self.email,
        'chips': self.chips,
        'balance': "$" + str("%.2f" % self.balance),
        'joined': self.joined.strftime("%M %d, %Y")
      }

class Games(db.Model):
  __tablename__ = 'Games'
  id = db.Column(db.Integer, primary_key=True)
  player_id = db.Column(db.String(80))
  timestamp = db.Column(db.DateTime)

  first_player = db.Column(db.Integer) # aka little blind - 0 for dealer 1 for player

  _moves = db.Column(db.String(255))

  _table_cards = db.Column(db.String(100))
  _dealer_cards = db.Column(db.String(40))
  _player_cards = db.Column(db.String(40))

  winner = db.Column(db.Integer) # 0 for dealer 1 for player
  pot = db.Column(db.Integer)

  _deck = Deck()

  def __init__(self, player_id):
    self.player_id = player_id

    self._dealer_cards = [self._deck.deal(), self._deck.deal()]
    self._player_cards = [self._deck.deal(), self._deck.deal()]
    self._table_cards = []

    self._moves = []

    self.timestamp = datetime.now(pytz.utc)

  def deal(self):
    if self._table_cards == []:
      self._table_cards = [self._deck.deal(), self._deck.deal(), self._deck.deal()]
    else:
      self._table_cards.append(self._deck.deal())

  # return -1 -> fold and 0 -> call or check and x > 0 -> raise by x
  # should take in many factors including past player behavior, cards in hand, cards on table, current bet
  def move(self):
    current_bet = moves[len(moves)-1] - moves[len(moves)-2]

    table_hand = Hand(self.table_cards)
    dealer_hand = Hand(self._dealer_cards + self._table_cards)

    table_score = table_hand.score()
    dealer_score = dealer_hand.score()

    return 0

  def determine_winner(self):
    pass

  @property
  def serialize(self):
    return {
      'id': self.id,
      'player_id': self.player_id,
      'pot': self.pot,
      'winner': self.winner,
      'table_cards': self.table_cards,
      'dealer_cards': self.dealer_cards,
      'player_cards': self.player_cards,
      'timestamp': self.timestamp.strftime("%b %d %I:%M %p")
    }
