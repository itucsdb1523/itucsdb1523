class CompetitionCollection:
    def __init__(self):
        self.competitions={}
        self.last_key=0

    def add_competitioner(self, competitioner):
        self.last_key += 1
        self.competitions[self.last_key] = competitioner

    def get_competitioner(self, key):
        return self.competitions[key]

    def get_competitioners(self):
        return sorted(self.competitioners.items())