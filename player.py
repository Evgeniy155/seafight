import regulars

from random import choice

from playerstrategy import PlayerStrategy
from playerstatistics import PlayerStatistic
from ship import Ship

class Player(object):
    def __init__(self):
        self.player_name = regulars.rdn_usr_name()
        self.strategy = PlayerStrategy()
        self.stat = PlayerStatistic()
        self.create_ships()

    def create_ships(self):
        self.ships = []
        buff_cord = []
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for ship in ships:
            if self.strategy.combinations[ship]:
                cords = choice(self.strategy.combinations[ship])
                overlay = regulars.set_halo(cords)
                self.strategy.data_cleaner(cords, overlay)
                buff_cord.append([ship, cords, overlay])
            else:
                self.strategy.reload()
                self.create_ships()
        for cords_for_unpack in buff_cord:
            ship, cords, overlay = cords_for_unpack
            self.ships.append(Ship(ship, cords, overlay))

    def shoot(self, cords):
        """Возвращает результат стрельбы по координатам"""
        for ship in self.ships:
            if cords in ship.cord:
                ship.shoots.append(cords)
                shoot_res = ship.get_state()
                return shoot_res
        else:
            return u'Мимо!'

    def reset_values(self):
        self.strategy.reset()
        self.stat.reset()
        self.ships = self.create_ships()
