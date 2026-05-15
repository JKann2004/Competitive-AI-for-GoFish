"""A French suited playing card class"""

from collections import namedtuple

# A named tuple that is the precursor to a French suited Card
_Card = namedtuple("_Card", ["rank", "suit"])


class Card(_Card):
    """French suited card"""

    ranks = (["Ace"] + [str(x) for x in range(2, 11)]
             + "Jack Queen King".split())
    suits = "♣️ ♥️ ♠️ ♦️".split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __str__(self):
        """Convert a card to a nicely formatted string"""
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        """Python representation of a Card"""
        return f"Card({self.rank}, {self.suit})"

    def __int__(self):
        """Return the numerical value of the rank of a given card."""
        return Card.value_dict[self.rank]