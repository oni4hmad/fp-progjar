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
        self.players['position'] = "200,100"

    def add_push(self, params=[]):
        pnum = params[0]
        curr_position = self.players['position']
        x, y = curr_position.split(',')
        try:
            if (pnum == '1'):
                self.players['position']=f"{int(x)+self.push_power},{y}"
                print(self.players['position'])
            elif (pnum == '2'):
                self.players['position']=f"{int(x)-self.push_power},{y}"
                print(self.players['position'])
            self.players.sync()
            return dict(status='OK', player=pnum, x=f'+{self.push_power}')
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
