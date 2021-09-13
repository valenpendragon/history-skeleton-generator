"""
Created in this form 04:04 on 02/09/2020.
Copyright (C) 2017, 2019, 2020  Jeffrey L. Scott

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This is the class library for Deck and Card classes.  There are a number of
classes in this library:

    Class AbstractCard: Abstract card class
        SubClass Ace: Store aces and their second value
        SubClass FaceCard: Stores face cards with their constant value of 10
        SubClass NumberCard: Stores cards with numberical values on the face
            that match the card's score value

    Class AbstractDeck: Object containing 52 cards, randomly shuffled with
        extra entropy. Note: Even with extra entropy, this is only random
        enough for a video game, not actual gambling.
        SubClass StdDeck: A single deck implementation of AbstractDeck
        SubClass CardShoe: A multideck card dealing shoe (1-8 decks)
            implementation of AbstactDeck

Both classes require Abstract Base Class. The Deck class requires the
random package in addition.
"""

import random as rd
from abc import ABC, abstractmethod


class AbstractCard(ABC):
    """
    AbstractCard(rank, suit) requires two arguments and creates this object.

    Should be used as a base class to create specific card types, such
    NumberCard, FaceCard, Ace, WildCard, etc. Some of these basic card types
    are included as subclasses.

    Methods
    -------
        __init__: Puts the rank and suit into the correct attributes, value
            is handled in the subclasses. Valid rank and suit checkes are
            made and will raise ValueError if incorrect. Subclasses should
            invoke this wits super().
        __str__ : returns string 'rank-suit'. Subclasses invoke with super().
        __repr__: abstractmethod only

    Attributes
    ----------
        self.rank: This is the rank of the card. Valid values are found in
            RANKS constant.
        self.suit: This is the card suit (Spades, Diamonds, Hearts, Clubs),
            represented by the first character of the name of the suit.
            Valid values are in SUITS constant.
        self.value: Initialized by subclasses only.
    """

    # Constants:
    RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    SUITS = ('S', 'D', 'H', 'C')
    FACECARDS = ('J', 'Q', 'K')
    NUMBERCARDS = ('2', '3', '4', '5', '6', '7', '8', '9', '10')

    # Methods
    def __init__(self, rank, suit):
        """
        Usage: AbstractCard(rank, suit) to instantiate a basic card object.

        This method will validate the rank and suit against constants RANKS
        and SUITS from the class. The card's value as part of a hand is left
        to subclasses. Invoke this abstract base class method via super()
        method to use its code.
        INPUTS: two strings, rank and suit
        OUTPUTS: none outside of creating the card object
        """
        if rank not in self.RANKS:
            print(f"AbstractCard: An invalid rank was supplied {rank}.")
            raise ValueError("Card objects must have a valid rank.") from None
            return None

        if suit not in self.SUITS:
            print(f"AbstractCard: An invalid suit was supplied {suit}.")
            raise ValueError("Card objects must have a valid suit.") from None
            return None
        self.rank = rank
        self.suit = suit
        self.value = None

    def __str__(self):
        """Return a three character string '{rank}-{suit}'."""
        return f"{self.rank}-{self.suit}"

    @abstractmethod
    def __repr__(self):
        """Method left to subclasses. This is an abstractmethod."""
        pass

    def __eq__(self, other):
        """
        Set the criteria for determining if 2 Cards are equal.

        Two Cards are considered equal if their ranks and suits match.
        """
        if (self.rank, self.suit) == (other.rank, other.suit):
            return True
        else:
            return False

    def __lt__(self, other):
        """
        Set the criteria for sorting one card before another different card.

        Sets the criteria of sorting cards first by rank, with the order
        determined by index in the constant RANKS. If the ranks are equal,
        the suits are compared, this time in reverse order, using SUITS.
        """
        # Eliminate equivalence first.
        if self == other:
            return False
        # Casting RANKS and SUITS as lists allows us to use the index() method
        # to determine their order. Since Spades is considered the highest
        # ranking suit, we need to reverse the order of SUITS.
        ranks = list(self.RANKS)
        suits = list(self.SUITS)
        suits.reverse()
        if ranks.index(self.rank) < ranks.index(other.rank):
            return True
        elif (self.rank == other.rank and
              suits.index(self.suit) < suits.index(other.suit)):
            return True
        else:
            return False

    def __le__(self, other):
        """
        Set the criteria for less than or equal to for Card objects.

        This is the last boolean we need to set to establish a clear order
        for Card objects. This can be used to apply these classes to other
        games besides Blackjack.
        """
        return self.__eq__(other) or self.__lt__(other)


class Ace(AbstractCard):
    """
    Usage: Ace(suit). Returns a object.

    This class uses the methods from AbstractCard and adds an extra attribute,
    high_value, to this object. Unlike other card objects, it only requires a
    suit as an argument.
    """

    # Methods
    def __init__(self, suit):
        """
        Usage: Ace(suit).

        This method calls super().__init__() to run checks on the suit and
        set the rank and suit.
        INPUT: one string, suit
        OUTPUTS: Card object
        """
        super().__init__(rank='A', suit=suit)
        self.value = 1
        self.high_value = 11

    def __str__(self):
        """Return a three character string 'A-{suit}'."""
        output = super().__str__()
        return output

    def __repr__(self):
        """Return a string of the class call."""
        return f"Ace({self.suit})"

    def __eq__(self, other):
        """
        Set the criteria for determining if 2 Cards are equal.

        Two Cards are considered equal if their ranks and suits match.
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        Set the criteria for sorting one card before another different card.

        Sets the criteria of sorting cards first by rank, then suit in the
        order that they appear in the RANKS and SUITS constants. This applies
        only to Card objects.
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        Set the criteria for less than or equal to for Card objects.

        This is the last boolean we need to set to establish a clear order
        for Card objects. This can be used to apply these classes to other
        games besides Blackjack.
        """
        return super().__le__(other)


class FaceCard(AbstractCard):
    """
    Usage: FaceCard(rank, suit). Keeps Card.value a constant for all objects.

    This class uses the methods from AbstractCard without adding any
    additional attributes.
    """

    # All face cards have a value of 10 in Blackjack.
    CARDVALUE = 10

    # Methods
    def __init__(self, rank, suit):
        """
        Usage: FaceCard(rank, suit).

        This method calls super().__init__() to run checks on the suit and
        set the rank and suit. It then sets the value attribute to constant
        CARDVALUE for this object type.
        INPUTS: strings, rank and suit
        OUTPUTS: Card object
        """
        if rank not in self.FACECARDS:
            print(f"FaceCard: An invalid rank was supplied {rank}.")
            raise ValueError("FaceCard.rank must be J, Q, or K") from None
            return None
        super().__init__(rank=rank, suit=suit)
        self.value = self.CARDVALUE

    def __str__(self):
        """Return a three character string '{rank}-{suit}'."""
        output = super().__str__()
        return output

    def __repr__(self):
        """Return a string of the class call."""
        return f"FaceCard({self.rank}, {self.suit})"

    def __eq__(self, other):
        """
        Set the criteria for determining if 2 Cards are equal.

        Two Cards are considered equal if their ranks and suits match.
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        Set the criteria for sorting one card before another different card.

        Sets the criteria of sorting cards first by rank, then suit in the
        order that they appear in the RANKS and SUITS constants. This applies
        only to Card objects.
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        Set the criteria for less than or equal to for Card objects.

        This is the last boolean we need to set to establish a clear order
        for Card objects. This can be used to apply these classes to other
        games besides Blackjack.
        """
        return super().__le__(other)


class NumberCard(AbstractCard):
    """
    Usage: NumberCard(rank, suit). These cards have numbers on the face.

    This class uses the methods from AbstractCard without adding any
    additional attributes.
    """

    # Methods
    def __init__(self, rank, suit):
        """
        Usage: NumberCard(rank, suit).

        This method calls super().__init__() to run checks on the suit and
        set the rank and suit. It then sets the value attribute.
        INPUTS: strings, rank and suit
        OUTPUTS: Card object
        """
        if rank not in self.NUMBERCARDS:
            print(f"NumberCard: An invalid rank was supplied {rank}.")
            raise ValueError("NumberCard.rank must be an integer") from None
            return None
        super().__init__(rank=rank, suit=suit)
        self.value = int(self.rank)

    def __str__(self):
        """Return a three character string '{rank}-{suit}'."""
        output = super().__str__()
        return output

    def __repr__(self):
        """Return a string of the class call."""
        return f"NumberCard({self.rank}, {self.suit})"

    def __eq__(self, other):
        """
        Set the criteria for determining if 2 Cards are equal.

        Two Cards are considered equal if their ranks and suits match.
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        Set the criteria for sorting one card before another different card.

        Sets the criteria of sorting cards first by rank, then suit in the
        order that they appear in the RANKS and SUITS constants. This applies
        only to Card objects.
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        Set the criteria for less than or equal to for Card objects.

        This is the last boolean we need to set to establish a clear order
        for Card objects. This can be used to apply these classes to other
        games besides Blackjack.
        """
        return super().__le__(other)


class AbstractDeck(list, ABC):
    """
    AbstractDeck(**kwrds), kwrds include num_decks=1 (optional).

    This class sets up the methods used to shuffle decks of cards that can
    contain more than one deck. The deck is composed of 52 Cards in the
    following numbers:
        4 Aces, 1 in each suit
        36 NumberCards, 9 for each suit
        12 FaceCards, 3 for each suit
        There are no jokers in Blackjack

    Methods
    -------
        __init__: returns a shuffled deck of 52 cards as a list with extra
            a few extra methods. Takes no arguments.
        __str__: inherited from list
        __repr__: inherited frorm list
        remove_top: synonym for pop(0)
        remaining_cards: returns a string showing number of cards out of
            self.size that remain
        Note: __len__ is inherited from List.

    Attributes
    ----------
        size: original size of this deck.
    """

    # Constants
    RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    SUITS = ('S', 'D', 'H', 'C')
    FACECARDS = ('J', 'Q', 'K')
    NUMBERCARDS = ('2', '3', '4', '5', '6', '7', '8', '9', '10')

    # Methods:
    def __init__(self, **kwrds):
        """
        AbstractDeck(**kwrds), kwrds include num_decks=1 (optional).

        This method generates a 52-card deck of Card objects that has been
        shuffled using rd.randint and rd.shuffle to create it. This process
        introduces extra entropy, but not enough for gambling purposes.
        INPUTS: **kwrds: num_decks, integer (optional), default=1
        OUTPUTS: Deck object containing 52 Card objects.
        """
        super().__init__(self)
        num_decks = 1
        # Checking keywords (kwrds)
        if 'num_decks' in kwrds:
            num_decks = kwrds['num_decks']
        self.size = 52 * num_decks
        # Next, we build the unshuffled deck
        for i in range(num_decks):
            for suit in self.SUITS:
                for rank in self.RANKS:
                    if rank == 'A':
                        card = Ace(suit)
                    elif rank in self.NUMBERCARDS:
                        card = NumberCard(rank, suit)
                    else:
                        card = FaceCard(rank, suit)
                    # deck.append(card)
                    self.append(card)
        rd.shuffle(self)
        # Now, we add extra entropy by using randint to do additional
        # reshuffles.
        for i in range(rd.randint(0, self.size)):
            rd.shuffle(self)

    def remove_top(self):
        """Remove the top card from a Deck object and returns this Card."""
        return self.pop(0)

    def remaining_cards(self):
        """Return a string with len(self) cards remain of self.size."""
        return f"{len(self)} of {self.size} cards remain"


class StdDeck(AbstractDeck, list, ABC):
    """Uses AbstractDeck to create a single 52 card deck."""

    def __init__(self, **kwrds):
        """
        Initialize a 52 card deck for blackjack.

        INPUTS: none. Optional integer, num_decks in keywords (not used)
        OUTPUTS: Deck object containing 52 Card objects.
        """
        # Standard decks have exactly 52 cards. We need to override a keyword
        # changing that.
        kwrds['num_decks'] = 1
        super().__init__(**kwrds)

    def remove_top(self):
        """Remove the top card from a Deck object and returns this card."""
        return super().remove_top()

    def remaining_cards(self):
        """Return a string with len(self) cards remain of self.size."""
        return super().remaining_cards()


class CardShoe(AbstractDeck, list, ABC):
    """
    CardShoe(**kwrds), kwrds include num_decks=6 (optional).

    Deck mimics the behavior of a multideck card dealing shoe. Contains
    multiples of 52-card decks with AbstractDeck behavior. The number of
    multiples is any integer greater than zero. The number of decks is
    included in keyward arguments to this class. The default of 6 is in line
    with the size most casinos use at regular blackjack tables.
    INPUTS: integer num_decks (optional), default 6
    OUTPUTS: Deck object
    """

    def __init__(self, **kwrds):
        """
        Create a multideck card dealing shoe with AbstractDeck behavior.

        Deck will contain multiples of 52 card decks before being shuffled
        a minimum of twice and a maximum of number of cards in the shoe.
        INPUTS: **kwrds (optional). num_decks, integer (default=6)
        OUTPUTS: Deck object of size num_decks * 52
        """
        # We need to get the higher default ready before passing kwrds to
        # the parent __init__.
        num_decks = 6
        if 'num_decks' not in kwrds:
            kwrds['num_decks'] = num_decks
        super().__init__(**kwrds)

    def remove_top(self):
        """Remove the top card from a Deck object and returns this card."""
        return super().remove_top()

    def remaining_cards(self):
        """Return a string with len(self) cards remain of self.size."""
        return super().remaining_cards()
