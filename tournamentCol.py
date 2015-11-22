class TournamentCol:
    def __init__(self):
        self.tournaments={}
        self.last_key=0

    def add_tournament(self, tournament):
        self.last_key += 1
        self.tournaments[self.last_key] = tournament

    def get_tournament(self, key):
        return self.tournaments[key]

    def get_tournaments(self):
        return sorted(self.tournaments.items())