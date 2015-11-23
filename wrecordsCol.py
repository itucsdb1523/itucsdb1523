class wrecordsCol:
    def __init__(self):
        self.worldrecords={}
        self.last_key=0

    def add_worldrecord(self, game):
        self.last_key += 1
        self.worldrecords[self.last_key] = game

    def get_worldrecord(self, key):
        return self.worldrecords[key]

    def get_worldrecords(self):
        return sorted(self.worldrecords.items())