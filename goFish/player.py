"""Generic Player class for Go Fish (cleaned from Blackjack version)"""

from uuid import uuid4

class Player:
    """A generic player class."""

    def __init__(self, name, player_id):
        self._name = name
        self._player_id = player_id

    @property
    def name(self):
        return self._name

    @property
    def player_id(self):
        return self._player_id

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self._name}', player_id='{self._player_id}')"


class GoFishPlayer(Player):
    """Player class specifically for Go Fish."""

    def __init__(self, name):
        super().__init__(name, uuid4())
        self.player_hand = []
        self.books = []

    def reset(self):
        """Reset player state for a new game."""
        self.player_hand = []
        self.books = []

    def has_rank(self, rank):
        """Check if player has at least one card of a rank."""
        return any(card.rank == rank for card in self.player_hand)

    def remove_rank(self, rank):
        """Remove and return all cards of a given rank."""
        matches = [c for c in self.player_hand if c.rank == rank]
        self.player_hand = [c for c in self.player_hand if c.rank != rank]
        return matches