class gameCol:
    def __init__(self):
        self.games={}
        self.last_key=0

    def add_game(self, game):
        self.last_key += 1
        self.games[self.last_key] = game

    def get_game(self, key):
        return self.games[key]

    def get_games(self):
        return sorted(self.games.items())