class medalCol:
    def __init__(self):
        self.medals={}
        self.last_key=0

    def add_medal(self, medal):
        self.last_key += 1
        self.medals[self.last_key] = medal

    def get_medal(self, key):
        return self.medals[key]

    def get_medals(self):
        return sorted(self.medals.items())