class recurveCollection:
    def __init__(self):
        self.recurvers={}
        self.last_key=0

    def add_recurver(self, recurver):
        self.last_key += 1
        self.recurvers[self.last_key] = recurver

    def get_recurver(self, key):
        return self.recurvers[key]

    def get_recurvers(self):
        return sorted(self.recurvers.items())