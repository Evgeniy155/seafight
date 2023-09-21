class PlayerStatistic(object):
    def __init__(self):
        self.score = 0
        self.step = 0
        self.ships_defeat = []
        self.tur_scores = 0

    def reset(self):
        self.score = 0
        self.step = 0
        self.ships_defeat = []