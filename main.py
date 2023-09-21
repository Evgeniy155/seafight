from copy import copy
from logging import basicConfig, INFO, info

from game import Game
from player import Player
from tournamentstatistic import TournaimentStatistic

basicConfig(format=u'[%(asctime)s]  %(message)s', level=INFO)


if __name__ == '__main__':
    turnaiment_player_counter = 512
    tour_stats = TournaimentStatistic()
    info(u'Начало турнира')
    tur_player_list = [Player() for player in range(turnaiment_player_counter)]
    # info(u'Список игроков: %s', ", ".join([x.player_name for x in tur_player_list]))
    tur_player_list_next_iter = []
    while len(tur_player_list) != 1:
        for player_ind in range(1, len(tur_player_list), 2):
            winner = Game(tur_player_list[player_ind - 1], tur_player_list[player_ind], tour_stats).game()
            tur_player_list_next_iter.append(winner)
        tur_player_list = copy(tur_player_list_next_iter)
        tur_player_list_next_iter = []
    else:
        info(u'Турнир выйграл: %s, набрал очков: %s', tur_player_list[0].player_name,
             tur_player_list[0].stat.tur_scores)
    med_step_all, med_step_win, med_step_looser, med_score_looser = tour_stats.count_middles()
    info(
        u'Статистика: \n\t1. Среднее количесво ходов (всех игроков): %.2f,\n\t2. Среднее количество ходов выйгравших игроков: %.2f,\n\t3. Среднее количество ходов проигравших игроков: %.2f,\n\t4. Среднее количество очков, которое набрали проигравшие: %.2f',
        med_step_all, med_step_win, med_step_looser, med_score_looser)
    res_strat = tour_stats.startegy_effect()
    for pl_stat in res_strat.keys():
        info(u'%s:', pl_stat)
        bf = []
        for strategy_com in res_strat[pl_stat]:
            if strategy_com not in bf:
                bf.append(strategy_com)
                info(u'%s: %s', ", ".join(strategy_com), res_strat[pl_stat].count(strategy_com))
