import regulars

from random import choice, shuffle
from copy import deepcopy

class PlayerStrategy(object):


    def __init__(self):
        self.turnaiment_player_counter = 512
        self.strategy_quota = [y for y in ["for_1_ship_left",
                                  "for_1_ship_right",
                                  "for_1_ship_top",
                                  "for_1_ship_bottom",
                                  "for_1_ship_center_horisontal",
                                  "for_1_ship_center_vertical",
                                  "for_1_ship_36",
                                  "random_12"] for _ in range(int(self.turnaiment_player_counter / 8))]
        shuffle(self.strategy_quota)
        self.alien_cords = []
        self.recomendation_pool = []
        self.succ_shoots = []
        self.ships_strategy_collocation = self.strategy_quota.pop()
        self.combinations = deepcopy(regulars.gen_cord(self.ships_strategy_collocation))
        self.steps_strategy = choice(list(regulars.STEPS_STRATEGY.keys()))
        self.steps_cords = deepcopy(regulars.STEPS_STRATEGY[self.steps_strategy])

    def get_crd_for_step(self):
        """Выбор координат для хода"""
        if self.recomendation_pool:
            crd = self.recomendation_pool.pop(0)
        elif self.steps_cords:
            shuffle(self.steps_cords)
            crd = self.steps_cords.pop(0)
        else:
            crd = choice(filter(lambda x: x not in self.alien_cords, regulars.CORD_10_10))
        if crd in self.recomendation_pool:
            self.recomendation_pool.remove(crd)
        elif crd in self.recomendation_pool:
            self.recomendation_pool.remove(crd)
        self.alien_cords.append(crd)
        return crd

    def return_shoot_state(self, state, crd, player2):
        """Стратегия дальнейщих ходов в зависимости от результата текущего хода"""
        if state == u'Попал!':
            if not self.recomendation_pool:
                crd_rec = [[crd[0] - 1, crd[1]], [crd[0] + 1, crd[1]], [crd[0], crd[1] - 1], [crd[0], crd[1] + 1]]
                crd_rec = filter(lambda x: 0 <= x[0] <= 9 and 0 <= x[1] <= 9, crd_rec)
                self.succ_shoots.append(crd)
                self.recomendation_pool.extend([crd for crd in crd_rec if crd not in self.alien_cords])
            else:
                crd_s1 = self.recomendation_pool[0]
                crd_s2 = self.succ_shoots[0]
                for ind in range(2):
                    if crd_s1[ind] != crd_s2[ind]:
                        if crd_s1[ind] > crd_s2[ind]:
                            crd_rec = [[crd_s1[ind] + 1, crd_s1[ind] + 2], [crd_s2[ind] - 1, crd_s2[ind] - 2]]
                        else:
                            crd_rec = [[crd_s1[ind] - 1, crd_s1[ind] - 2], [crd_s2[ind] + 1, crd_s2[ind] + 2]]
                        crd_rec = filter(lambda x: 0 <= x[0] <= 9 and 0 <= x[1] <= 9, crd_rec)
                        self.recomendation_pool.extend([crd for crd in crd_rec if crd not in self.alien_cords])
        elif state == u'Убил!':
            for ship in player2.ships:
                if crd in ship.cord:
                    self.alien_cords.extend([crd for crd in ship.halo if crd not in self.alien_cords])
                    self.steps_cords = filter(lambda x: x not in ship.halo and x not in self.alien_cords,
                                              self.steps_cords)
            self.recomendation_pool = []
            self.succ_shoots = []

    def data_cleaner(self, cords, overlay):
        """Удаляет использованные комбинации из словаря комбинаций пользователя
        используется при создании кораблей"""
        del_index = {}
        for ship in self.combinations.keys():
            del_index[ship] = []
            for ind, crd_pack in enumerate(self.combinations[ship]):
                for crd in cords + overlay:
                    if crd in crd_pack and ind not in del_index[ship]:
                        del_index[ship].append(ind)
        for ship in del_index.keys():
            for ind_for_del in reversed(del_index[ship]):
                del self.combinations[ship][ind_for_del]

    def reload(self):
        self.combinations = deepcopy(regulars.gen_cord(self.ships_strategy_collocation))

    def reset(self):
        self.alien_cords = []
        self.recomendation_pool = []
        self.succ_shoots = []
        self.combinations = deepcopy(regulars.gen_cord(self.ships_strategy_collocation))
        self.steps_strategy = choice(regulars.STEPS_STRATEGY.keys())
        self.steps_cords = deepcopy(regulars.STEPS_STRATEGY[self.steps_strategy])