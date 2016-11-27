# -*- codgin: utf-8 -*-
import random

class Player(object):
    def __init__(self, borad):
        self.gameBorad = borad

    def random_action(self):
        succ_move = False
        while not succ_move:
            self.gameBorad.restore_borad_info()
            nextAction = self.gameBorad.actionTable[ random.randint(0,3) ]
            succ_move = nextAction(self.gameBorad.simuBorad)

        nextAction(self.gameBorad.borad)
        self.gameBorad.save_borad_info()

    def action(self):
        self.random_action()

