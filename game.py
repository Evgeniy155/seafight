from random import choice
from logging import basicConfig, INFO, info

class Game(object):
    def __init__(self, player1, player2, tour_stats):
        # info(u'Начало игры')
        self.player_list = [player1, player2]
        self.curr_player = None
        self.player_log_list()
        self.tour_stats = tour_stats

    def player_log_list(self):
        # info(u'Игроки: %s', ", ".join([x.player_name for x in self.player_list]))
        pass

    def game(self):
        self.tour_stats.game_id += 1
        # Выбираем игрока для первого хода
        if self.curr_player is None:
            self.curr_player = choice(self.player_list)
        # Получаем координаты для хода
        crd_for_shoot = self.curr_player.strategy.get_crd_for_step()
        # Выделяем второго игрока из списка
        player2 = filter(lambda x: x != self.curr_player, self.player_list)[0]
        # Ходим и сохраняем результаты хода
        shoot_res = player2.shoot(crd_for_shoot)
        # Передаём результаты хода ходившему игроку
        # logging.info(u'Ходит: %s, координаты: %s, статус: %s', self.curr_player.player_name, crd_for_shoot, shoot_res)
        self.curr_player.strategy.return_shoot_state(shoot_res, crd_for_shoot, player2)
        self.curr_player.stat.step += 1
        if shoot_res in [u'Убил!', u'Попал!']:
            self.curr_player.stat.score += 1
        # Меняем счётчик текущего пользователя, если ходивший промазал
        if shoot_res == u'Мимо!':
            self.curr_player = player2
        # Конец игры и вывод статистики
        if shoot_res == u'Убил!':
            self.curr_player.stat.ships_defeat.append(1)
            if len(self.curr_player.stat.ships_defeat) == 10:
                # info(u'Выйграл: %s', self.curr_player.player_name)
                # info(u'%s', ", ".join([str(x.player_name) + u" набрал очков:  " + str(x.scores) + u", ходов: " + str(x.steps) for x in self.player_list]))
                # Сбрасываем счётчики
                self.curr_player.stat.tur_scores += self.curr_player.stat.score
                self.tour_stats.get_stats(self.player_list)
                self.curr_player.reset_values()
                # info(u'------------------')
                return self.curr_player
        # Если игра продолжается, то перезапускаем функцию game()
        return self.game()