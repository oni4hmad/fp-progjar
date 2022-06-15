import os
import json
import base64
from glob import glob
import shelve

#asumsi, hanya ada player 1, 2 , 3

class PlayerServerInterface:
    def __init__(self):
        self.push_power = 5
        self.players = shelve.open('g.db',writeback=True)

        # inital position
        self.inital_x, self.initial_y = 200, 100
        self.win_offset = 200
        self.players['position'] = f"{self.inital_x},{self.initial_y}"

        # win state
        # True = win, False = lose
        self.is_p1_win = None
        self.is_p2_win = None

    def add_push(self, params=[]):
        pnum = params[0]
        curr_position = self.players['position']
        x, y = curr_position.split(',')
        try:
            if (pnum == '1'):
                x = int(x)+self.push_power
                self.players['position']=f"{x},{y}"
                print(self.players['position'])
                if (x > self.inital_x+self.win_offset):
                    self.is_p1_win = True
                    self.is_p2_win = False
            elif (pnum == '2'):
                x = int(x)-self.push_power
                self.players['position']=f"{x},{y}"
                print(self.players['position'])
                if (x < self.inital_x-self.win_offset):
                    self.is_p1_win = False
                    self.is_p2_win = True
            self.players.sync()
            return dict(status='OK', player=pnum, x=f'+{self.push_power}')
        except Exception as e:
            return dict(status='ERROR')

    def get_is_win(self, params=[]):
        pnum = params[0]
        is_win = self.is_p1_win if pnum == '1' else self.is_p2_win
        print('is_win', is_win)
        try:
            return dict(status='OK', player=pnum, is_win=is_win)
        except Exception as e:
            return dict(status='ERROR')

    def get_location(self, params=[]):
        pnum = params[0]
        try:
            return dict(status='OK', location=self.players['position'])
        except Exception as ee:
            return dict(status='ERROR')



if __name__=='__main__':
    p = PlayerServerInterface()
    p.add_push(['1'])
    print(p.get_location('1'))
    p.add_push(['2'])
    print(p.get_location('2'))

    print(p.get_is_win(['1']))
    print(p.get_is_win(['2']))