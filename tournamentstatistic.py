from copy import deepcopy

class TournaimentStatistic(object):
    def __init__(self):
        self.game_id = 0
        self.step_all = []
        self.step_winners = []
        self.scores_loosers = []
        self.step_loosers = []
        self.players_copy_list = []

    def get_stats(self, player_list):
        self.players_copy_list.extend([deepcopy(player) for player in player_list])

    def count_middles(self):
        self.step_all = [player.stat.step for player in self.players_copy_list]
        self.step_winners = [player.stat.step for player in self.players_copy_list if
                             len(player.stat.ships_defeat) == 10]
        self.step_loosers = [player.stat.step for player in self.players_copy_list if
                             len(player.stat.ships_defeat) != 10]
        self.scores_loosers = [player.stat.score for player in self.players_copy_list if
                               len(player.stat.ships_defeat) != 10]
        return sum(self.step_all) / float(len(self.step_all)), sum(self.step_winners) / float(
            len(self.step_winners)), sum(self.step_loosers) / float(len(self.step_loosers)), sum(
            self.scores_loosers) / float(len(self.scores_loosers))

    def startegy_effect(self):
        report_strategy = {u"Победители": [], u"Проигравшие": []}
        for player in self.players_copy_list:
            pl_stat = ""
            if len(player.stat.ships_defeat) == 10:
                pl_stat = u"Победители"
            else:
                pl_stat = u"Проигравшие"
            report_strategy[pl_stat].append(
                [player.strategy.ships_strategy_collocation, player.strategy.steps_strategy])
        return report_strategy