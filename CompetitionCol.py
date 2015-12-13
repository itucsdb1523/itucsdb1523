class CompetitionCollection:
    def __init__(self):
        self.competitions={}
        self.last_key=0

    def add_competition(self, competition):
        self.last_key += 1
        self.competitions[self.last_key] = competition

    def get_competition(self, key):
        return self.competitions[key]

    def get_competitions(self):
        return sorted(self.competitions.items())