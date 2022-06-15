import os
import json
import base64
from glob import glob
import shelve


# asumsi, hanya ada player 2 player

class PlayerServerInterface:

    def __init__(self):
        self.push_power = 5
        self.players = shelve.open('g.db', writeback=True)

        # inital position
        self.inital_x, self.initial_y = 200, 100
        self.win_offset = 170
        self.players['position'] = f"{self.inital_x},{self.initial_y}"

        # current registered player
        self.incoming_players = []

        # game state
        self.is_started = False

        # win state
        # True = win, False = lose
        self.is_p1_win = None
        self.is_p2_win = None

    def add_push(self, params=[]):
        player_id = params[0]
        curr_position = self.players['position']
        x, y = curr_position.split(',')
        try:
            if (player_id == self.incoming_players[0]):
                x = int(x) + self.push_power
                self.players['position'] = f"{x},{y}"
                print(self.players['position'])
                if (x > self.inital_x + self.win_offset):
                    self.is_started = False
                    self.is_p1_win = True
                    self.is_p2_win = False
            elif (player_id == self.incoming_players[1]):
                x = int(x) - self.push_power
                self.players['position'] = f"{x},{y}"
                print(self.players['position'])
                if (x < self.inital_x - self.win_offset):
                    self.is_started = False
                    self.is_p1_win = False
                    self.is_p2_win = True
            self.players.sync()
            return dict(status='OK', player=player_id, x=f'+{self.push_power}')
        except Exception as e:
            return dict(status='ERROR')

    def get_is_win(self, params=[]):
        try:
            player_id = params[0]
            is_win = self.is_p1_win if player_id == self.incoming_players[0] else self.is_p2_win
            return dict(status='OK', player=player_id, is_win=is_win)
        except Exception as e:
            return dict(status='ERROR')

    def get_location(self, params=[]):
        player_id = params[0]
        try:
            return dict(status='OK', location=self.players['position'])
        except Exception as ee:
            return dict(status='ERROR')

    def register_id(self, params=[]):
        player_id = params[0]
        if not player_id in self.incoming_players and len(self.incoming_players) < 2:
            print('incodming player id', player_id)
            self.incoming_players.append(player_id)
            player_type = 'p1' if len(self.incoming_players) == 1 else 'p2'
            if len(self.incoming_players) >= 2: self.start_game()
            try:
                return dict(status='OK', is_success=True, player_type=player_type)
            except Exception as ee:
                return dict(status='ERROR')
        else:
            try:
                return dict(status='OK', is_success=False, msg="There's already 2 players")
            except Exception as ee:
                return dict(status='ERROR')

    def get_is_started(self, params=[]):
        try:
            return dict(status='OK', is_started=self.is_started)
        except Exception as ee:
            return dict(status='ERROR')

    def start_game(self):
        # reset game state
        self.is_p1_win = None
        self.is_p2_win = None
        self.players['position'] = f"{self.inital_x},{self.initial_y}"

        # set started
        self.is_started = True

    def disconnect(self, params=[]):
        player_id = params[0]
        if player_id in self.incoming_players:
            self.incoming_players.remove(player_id)
            self.is_p1_win = True
            self.is_p2_win = True
            self.is_started = False
        try:
            return dict(status='OK', is_disconnected=True)
        except Exception as ee:
            return dict(status='ERROR')

    # def maintain_connection(self, params=[]):
    #     player_id = params[0]

if __name__ == '__main__':
    p = PlayerServerInterface()
    p.add_push(['1'])
    print(p.get_location('1'))
    p.add_push(['2'])
    print(p.get_location('2'))

    print(p.get_is_win(['1']))
    print(p.get_is_win(['2']))
