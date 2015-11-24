class SponsorCollection:
    def __init__(self):
        self.sponsors={}
        self.last_key=0

    def add_sponsor(self, sponsor):
        self.last_key += 1
        self.sponsors[self.last_key] = sponsor

    def get_sponsor(self, key):
        return self.sponsors[key]

    def get_sponsors(self):
        return sorted(self.sponsors.items())