class GoFishBot:

    def __init__(self, ranks):
        self.ranks = ranks
        self.probabilities = {rank: 0.30 for rank in ranks}
        self.minimum_counts = {rank: 0 for rank in ranks}
        self.bot_books = set()

    def clamp(self, value):
        return max(0.0, min(1.0, value))

    def player_asked_bot(self, rank, cards_given=0):
        self.minimum_counts[rank] = max(self.minimum_counts[rank], 1)

        if cards_given > 0:
            self.minimum_counts[rank] += cards_given
            self.probabilities[rank] = self.clamp(self.probabilities[rank] + 0.25 + (0.25 * cards_given))
        else:
            self.probabilities[rank] = self.clamp(self.probabilities[rank] + 0.15)

    def bot_asked_player(self, rank, cards_received=0):
        if cards_received > 0:
            self.minimum_counts[rank] = max(0, self.minimum_counts[rank] - cards_received)
            self.probabilities[rank] = self.clamp(self.probabilities[rank] * 0.35)
        else:
            self.probabilities[rank] = self.clamp(self.probabilities[rank] * 0.80)

    def bot_completed_book(self, rank):
        self.probabilities[rank] = 0.0
        self.minimum_counts[rank] = 0

        self.bot_books.add(rank)

    def choose_rank(self, hand):
        if not hand:
            return None
        counts = {}
        for card in hand:
            counts[card.rank] = counts.get(card.rank, 0) + 1
        def usefulness(rank):
            c = counts.get(rank, 0)
            if c >= 3: return 3.0
            if c == 2: return 1.7
            if c == 1: return 0.8
            return 0.1

        best_rank = None
        best_score = -1

        for rank in counts:
            belief = self.probabilities[rank]
            belief += self.minimum_counts[rank] * 0.15
            score = belief * usefulness(rank)
            if score > best_score:
                best_score = score
                best_rank = rank
        return best_rank

    def show_probabilities(self):
        print("\n--- PLAYER RANK PROBABILITY     ---\n")
        ordered = sorted(self.ranks, key=lambda r: self.probabilities[r], reverse=True)
        for rank in ordered:
            prob = self.probabilities[rank]
            minimum = self.minimum_counts[rank]
            print(
                f"{rank}: "
                f"belief={prob:.2%}, "
                f"minimum={minimum}"
            )