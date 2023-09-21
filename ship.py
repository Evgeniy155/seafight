class Ship(object):
    def __init__(self, ship_type, cord, halo):
        self.ship_type = ship_type
        self.cord = cord
        self.halo = halo
        self.shoots = []
        self.state = u'Цел'

    def get_state(self):
        if len(self.shoots) == self.ship_type:
            self.state = u'Убил!'
        else:
            self.state = u'Попал!'
        return self.state