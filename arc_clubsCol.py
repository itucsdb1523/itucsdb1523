class ClubCollection:
    def __init__(self):
        self.clubs={}
        self.last_key=0

    def add_club(self, club):
        self.last_key += 1
        self.clubs[self.last_key] = club

    def get_club(self, key):
        return self.clubs[key]

    def get_clubs(self):
        return sorted(self.clubs.items())
