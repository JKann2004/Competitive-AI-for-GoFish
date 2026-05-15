import random
from collections import Counter

from goFish import player
from goFish import card
from goFish.bot import GoFishBot

class GoFishGame:

    def __init__(self):
        self.player = player.GoFishPlayer(input("Enter your name: "))
        self.opponent = player.GoFishPlayer("Bot")

        self.deck = self._create_deck()

        self.bot = GoFishBot(card.Card.ranks)

        self.sort_hand(self.player)
        self.sort_hand(self.opponent)

    def sort_hand(self, player_obj):
        player_obj.player_hand.sort(key=lambda c: card.Card.ranks.index(c.rank))

    def add_card(self, player_obj, card_obj):
        player_obj.player_hand.append(card_obj)
        self.sort_hand(player_obj)

    def _create_deck(self):
        deck = []
        for rank in card.Card.ranks:
            for suit in card.Card.suits:
                deck.append(card.Card(rank, suit))
        random.shuffle(deck)
        return deck

    def draw(self, p):
        if self.deck:
            c = self.deck.pop(0)
            self.add_card(p, c)

    # Completed a book (4 cards of the same rank)
    def check_books(self, p):
        counts = Counter(c.rank for c in p.player_hand)
        for rank, count in counts.items():
            if count == 4:
                print(f"{p.name} completed a book of {rank}!")
                p.books.append(rank)
                p.player_hand = [
                    c for c in p.player_hand
                    if c.rank != rank
                ]
                if p == self.opponent:
                    self.bot.bot_completed_book(rank)
                self.sort_hand(p)

    def game_over(self):
        return len(self.player.books) + len(self.opponent.books) == 13

    def play(self):
        for _ in range(7):
            self.draw(self.player)
            self.draw(self.opponent)

        turn = 0

        while not self.game_over():
            current = self.player if turn == 0 else self.opponent
            opponent = self.opponent if turn == 0 else self.player

            print(f"\n{current.name}'s turn")

            if current == self.player:
                self.bot.show_probabilities()
                print("Your hand:", [c.rank for c in current.player_hand])

                while True:
                    rank = input("Ask for a rank: ").strip().title()
                    if current.has_rank(rank):
                        break
                    print("You must choose a rank you have!")

                self.bot.player_asked_bot(rank, cards_given=0)

                print("-------------------------")

            else:
                self.bot.show_probabilities()
                rank = self.bot.choose_rank(current.player_hand)
                if rank is None:
                    print("AI has no cards. Skipping turn.")
                    turn = 1 - turn
                    continue
                print(f"AI asks for {rank}")

                print("-------------------------")

            if opponent.has_rank(rank):
                print(f"{opponent.name} has {rank}!")
                cards = opponent.remove_rank(rank)
                for c in cards:
                    self.add_card(current, c)

                # Update bot beliefs
                if current == self.player:
                    # Human asked successfully
                    self.bot.player_asked_bot(rank, cards_given=len(cards))
                else:
                    # AI asked successfully
                    self.bot.bot_asked_player(rank, cards_received=len(cards))

                self.check_books(current)

            else:
                print(f"{opponent.name} does not have {rank}")
                print("Go Fish!")
                self.draw(current)
                print(f"{current.name} drew a card")

                if current == self.player:
                    # Human asked and failed
                    self.bot.player_asked_bot(rank, cards_given=0)
                else:
                    # AI asked and failed
                    self.bot.bot_asked_player(rank, cards_received=0)

                self.check_books(current)
                turn = 1 - turn

    def run(self):
        self.play()
        print("\nGame Over!")
        print(f"{self.player.name}: {len(self.player.books)} books")
        print(f"{self.opponent.name}: {len(self.opponent.books)} books")
        return 0