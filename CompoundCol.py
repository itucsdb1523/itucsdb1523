class CompoundCollection:
    def __init__(self):
        self.compounders={}
        self.last_key=0

    def add_compounder(self, compounder):
        self.last_key += 1
        self.compounders[self.last_key] = compounder

    def get_compounder(self, key):
        return self.compounders[key]

    def get_compounders(self):
        return sorted(self.compounders.items())