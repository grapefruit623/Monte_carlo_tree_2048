# -*- codgin: utf-8 -*-
import cProfile
import os
import time
import copy
import threading

from baseClass.Borad_class import Borad
from baseClass.Logger_class import Logger
from baseClass.Player_class import Player

from monte_carlo_tree import Monte_Carlo_Player
from Gui import GuiThread

class Game(threading.Thread):
    def __init__(self, borad=None, player=None):
        super().__init__()
        self.gamePlayer = player
        self.gameBorad = borad
        self.logger = Logger()
        self.recordBorad = None
        self.dataQueue = None

    def run(self):
        self.gamePlayer.init_game()
        while not self.gameBorad.isEnd( self.gameBorad.borad ):
            # self.logger.printBorad('node', self.gameBorad.borad)
            # self.dataQueue.put({'board':self.gameBorad.borad, 'action':'cur'})
            # time.sleep(0.1)            
            self.recordBorad = copy.deepcopy(self.gameBorad.borad)
            actionName = self.gamePlayer.action()
            self.logger.recordBorad_and_Action(self.recordBorad, actionName)
            self.logger.printBorad(actionName, self.gameBorad.borad)
            self.dataQueue.put({'board':self.gameBorad.borad, 'action':actionName})
            time.sleep(0.1)            
            loc = self.gameBorad.random_blocks(self.gameBorad.borad)
            self.logger.printBoradWithColor(loc, self.gameBorad.borad)
            self.dataQueue.put({'board':self.gameBorad.borad, 'action':'random'})
            time.sleep(0.1)            
        else:
            print ('Game finish')
            print (self.gameBorad.borad)
            if 2048 in self.gameBorad.borad:
                print ('Winner!')
            else:
                print ('Loser..')

def play2048():
    b = Borad()
    m = Monte_Carlo_Player(borad=b)
    g = Game(borad=b, player=m)
    gui = GuiThread(gameCtrl=g)
    gui.start()

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
    # cProfile.runctx('play2048()', globals(), locals())
    play2048()
