"""
Manages all data user in card game 'war'

Clases Card, Hand and Player are models for objects used in the game.

This project was derived withing solving task in beautiful Udemy course
'Python and Django Full Stack Web Developer Bootcamp' by Jose Portilla.
https://www.udemy.com/python-and-django-full-stack-web-developer-bootcamp/learn/

This module demonstrates some Python OOP concepts and also functional
programming approach.

There are some features you can find here:
class,
inheritance,
method overiding,
calling 'super',
@property,
raise and handle Exceptions,
pass-by-reference,
iterator example,
generator,
@decarator,
*args, **kwargs,
list comprehension,
Python packaging,
modules,
__slots__,
magic functions,
print formatting,
documentation,
and much more...

Hope I'll expand this with:
implementing MVC (sounds like a joke but it worth)
@staticmethod and @classmethod (first in the row)
__hash__
implement decorator for class as once I've found in explanation about ABC
wrap with tests

Thanks a lot!


"""

from functools import wraps

# from collections import Iterable
# Python_Level_Two/playground/model.py:2: DeprecationWarning: Using or
# importing the ABCs from 'collections' instead of from 'collections.abc'
# is deprecated, and in 3.8 it will stop working
from collections.abc import Iterable

SUITE = ['H', 'D', 'S', 'C']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card():
    """
    Class represents playing card

    Card Class represent playing card of French card suits.
    Here is a link to decription for the popular French cards:
    https://en.wikipedia.org/wiki/Playing_card

    Allowed permissive non-case sensitive cards creation
    with type conversion:
    # card_kc == Card("K","c")
    # print(card_kc)          # >> CK
    # print(Card("j","d") == Card("J","C"))   # >> True
    # print(Card("j","d") == Card("10","c"))  # >> False
    # print(Card("j","d") == Card(10,"c"))    # >> False

    Args:
        arg (str): The arg is used for...
        *args: The variable arguments are used for...
        **kwargs: The keyword arguments are used for...

    Attributes:
        rank (str): Rank of the card, could be ono of the
                    ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                    'J', 'Q', 'K', 'A'],
        suite (str): Suit of the card,
                     one of the value in ['H', 'D', 'S', 'C']
        covered (boolean): Presents hidden or opened card,

    """

    def __init__(self, rank, suite, covered=False):
        """
        Initiates Card

        Raises:
            ValueError: Given rank or suite does not fit to French cards deck

        """
        if str(rank).upper() not in RANKS:
            raise ValueError("Rank {} is not recognized!".format(rank))
        self.rank = str(rank).upper()
        if suite.upper() not in SUITE:
            raise ValueError("Suite {} is not recognized!".format(suite))
        self.suite = suite.upper()
        self.covered = covered

    def hide_covered_cards(f):
        """
        Decorator for presentation of the covered card and mark it as uncovered

        Hide presentation of the covered card within current representation and
        mark it as uncovered to be shown openly later.

        More detaled information about decorators:
        https://realpython.com/primer-on-python-decorators/

        Example of usage:

        print("--Hide_covered_cards decorator--")
        card_as = Card("A","S")  # default is face-up, covered=False
        print(card_as.rank, card_as.suite)
        card_kd = Card("K","D", covered=True)

        print("--Presentation of the covered card 'King of Dimonds'--")
        print(card_as) # >> SA
        print(card_kd) # >> XX

        print("--This time 'King of Dimonds'is open--")
        print(card_as) # >> SA
        print(card_kd) # >> DK
        print("--Hide_covered_cards decorator end--")

        """

        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            Accepting values withing inner function
            and returning values.

            Some usefull walk through arguments and values:

            print(type(args), args)
            >>
            <class 'tuple'> (<__main__.Card object at 0x7fb3522f9be0>,)

            print(args[0].covered)
            >>
            False # or True, depends on 'covered' value

            print(type(kwargs), kwargs)
            >>
            <class 'dict'> {}

            """
            undecoreted = f(*args, **kwargs)

            if undecoreted[0]:
                args[0].covered = False # unhide card for later usage openly
                return "XX"             # hide presentation of the card
            else:
                return "".join([undecoreted[1], undecoreted[2]])
        return wrapper


    @hide_covered_cards
    def __str__(self):
        # return " ".join([self.suite, self.rank])  # gives something like: S A
        # return "".join([self.covered, self.suite, self.rank])  # SA
        return [self.covered, self.suite, self.rank]


    def __eq__(self, other):
        if isinstance(other, Card):
            return RANKS.index(self.rank) == RANKS.index(other.rank)
        else:
            raise TypeError("Could not compare Card and {}".format(type(other)))

    def __gt__(self, other):
        if isinstance(other, Card):
            return RANKS.index(self.rank) > RANKS.index(other.rank)
        else:
            raise TypeError("Could not compare Card and {}".format(type(other)))

    def __lt__(self, other):
        if isinstance(other, Card):
            return RANKS.index(self.rank) < RANKS.index(other.rank)
        else:
            raise TypeError("Could not compare Card and {}".format(type(other)))


class Hand:
    '''
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand. There should be an add and remove card method here.

    Attributes:
        _cards (Card): List of cards

    Presenting '@propery' for adding and retrieving cards.
    Here usage of the some 'magic' functions shown.

    Hand class implements iteration.

    Controls quantity of the Cards if requested some with draw_cards()

    Cards alowed to be added from just a Card or from iterables of the Cards

    '''

    def __init__(self, cards=None):
        self._cards = []


    def __str__(self):
        # return " ".join(list(\
        #   str(x) for x in ["Hand, id:", id(self),
        #   ", items:", len(self._cards)]) + list(str(x) for x in self._cards))

        return f"Hand, id: {id(self)}, items: {len(self._cards)} :\
            {*list(str(x) for x in self._cards),} "
            # https://www.python.org/dev/peps/pep-0498/
            # https://realpython.com/python-string-formatting/

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, new_card):
        # print(f"About adding to deck {type(new_card)}: {new_card}")
        if isinstance(new_card, Card):
            self._cards.append(new_card)
        else:
            for element in new_card:
                if isinstance(element, Card):
                    self._cards.append(element)
                else:
                    for card in element:
                        if isinstance(card, Card):
                            self._cards.append(card)
                        else:
                            raise TypeError("Could not add {} to Cards deck".
                            format(type(card)))
        # https://www.w3schools.com/python/python_ref_list.asp

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._cards) == 0:
            raise StopIteration
        return self._cards.pop(0)

    def draw_cards(self, num=1):
        """

        Args:
            num (int): The amount of Cards to be drawn

        Raises:
            ValueError: Hand could not put nesessary amount of the Cards

        Returns:
            res(list): List of the Cards

        """
        res = []
        try:
            for i in range(num):
                res.append(next(self))
            return res
        except StopIteration:
            # res = self._cards.copy()
            self._cards.clear()
            raise ValueError("Not enough cards")

        except Exception as e:
            print("Exception {}, {}".format(type(e), e))


class Player(Hand):
    """
    Player class represents cars player operating with cards_deck

    Here are some concepts shown:
        __slots__ for reducing memory utilisation
        Using 'super' for caling parent class method
        Different presentation of the instances with str() and repr()

    Attributes:
        arg (str): Name of the player

    """
    __slots__ = "_name", "_cards"
    def __init__(self, name=None):
        self._name = name
        super().__init__(self)

    @property
    def name():
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __str__(self):
        return f"Player {self._name} with {len(self.cards)} cards"

    def __repr__(self):
        """

    https://stackoverflow.com/questions/1436703/difference-between-str-and-repr

        """
        return f"Player {self._name} with {self.cards} cards"


def cards_generator():
    """
    Cards generator

    Presnts usage of generators in Python
    Generate pseudorandom deck of the cards

    Yields:
        random Card

    """
    from random import shuffle
    cards = []
    for s in SUITE:
        for r in RANKS:
            cards.append(Card(r, s))
    shuffle(cards)
    for card in cards:
        yield card

def init_game():
    """
    Creates table and players for 'war' card game

    Returns:
        table, players(tuple):
            table(Player): Given with distinctive name 'Table'

            players(list of Player): Players are given with default names,
                and dealled with 26 Cards each

    """
    cards_deck = cards_generator()
    players = list(Player(x) for x in ("PlayerA","PlayerB"))
    for player in players:
        player.cards = list(next(cards_deck) for x in range (26))

    table = Player("Table")

    return table, players

if __name__ =="__main__":
    print("Please import classes from this module or init_game()")
