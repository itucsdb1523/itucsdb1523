class CompoundTeamCollection:
    def __init__(self):
        self.compoundteams={}
        self.last_key=0

    def add_compoundteam(self, compoundteam):
        self.last_key += 1
        self.compoundteams[self.last_key] = compoundteam

    def get_compoundteam(self, key):
        return self.compoundteams[key]

    def get_compoundteams(self):
        return sorted(self.compoundteams.items())