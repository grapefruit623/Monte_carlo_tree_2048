# -*- codgin: utf-8 -*-
import cProfile
import os
import time
import copy

from baseClass.Borad_class import Borad
from baseClass.Logger_class import Logger
from baseClass.Player_class import Player

from monte_carlo_tree import Monte_Carlo_Player

class Game(object):
    def __init__(self, borad=None, player=None):
        self.gamePlayer = player
        self.gameBorad = borad
        self.logger = Logger()
        self.recordBorad = None

    def run(self):
        self.gamePlayer.init_game()
        while not self.gameBorad.isEnd( self.gameBorad.borad ):
            self.logger.printBorad('node', self.gameBorad.borad)
            self.recordBorad = copy.deepcopy(self.gameBorad.borad)
            actionName = self.gamePlayer.action()
            self.logger.recordBorad_and_Action(self.recordBorad, actionName)
            self.logger.printBorad(actionName, self.gameBorad.borad)
            loc = self.gameBorad.random_blocks(self.gameBorad.borad)
            self.logger.printBoradWithColor(loc, self.gameBorad.borad)
        else:
            print ('Game finish')
            print (self.gameBorad.borad)
            if 2048 in self.gameBorad.borad:
                return 1
            else:
                return 0

def play2048():
    b = Borad()
    m = Monte_Carlo_Player(borad=b)
    g = Game(borad=b, player=m)
    totals = 1 
    wins = 0.0
    for i in range(totals):
        print ('{0} games'.format(i))
        wins += g.run()
    print ('Win rate: ', wins/totals)

def unit_test():
    b = Borad()
    m = Monte_Carlo_Player(borad=b)
    g = Game(b, m)
    g.gamePlayer.init_game()
    print (g.gameBorad.borad)
    print ('-'*5)
    g.gameBorad.moveRight(g.gameBorad.borad)
    print (g.gameBorad.borad)

if __name__ == '__main__':
    # cProfile.runctx('unit_test()', globals(), locals())
    play2048()
