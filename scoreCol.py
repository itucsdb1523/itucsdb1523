class ScoreCol:
    def __init__(self):
        self.scores={}
        self.last_key=0

    def add_score(self, score):
        self.last_key += 1
        self.scores[self.last_key] = score

    def score(self, key):
        del self.scores[key]

    def get_score(self, key):
        return self.scores[key]
    
    def get_scores(self):
        return sorted(self.scores.items())