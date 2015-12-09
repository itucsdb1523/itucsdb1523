class infoCollection:
    def __init__(self):
        self.informations={}
        self.last_key=0

    def add_information(self, information):
        self.last_key += 1
        self.informations[self.last_key] = information

    def get_information(self, key):
        return self.informations[key]

    def get_informations(self):
        return sorted(self.informations.items())