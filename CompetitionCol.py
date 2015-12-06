class CompetitionCollection:
    def __init__(self):
        self.competitioners={}
        self.last_key=0

    def add_competitioner(self, competitioner):
        self.last_key += 1
        self.competitioners[self.last_key] = competitioner

    def get_competitioner(self, key):
        return self.competitioners[key]

    def get_competitioners(self):
        return sorted(self.competitioners.items())