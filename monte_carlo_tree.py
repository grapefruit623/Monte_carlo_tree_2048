from datetime import datetime
import math
import copy
import random
import numpy as np
import cProfile
import os
import time

class Logger(object):
    def __init__(self):
        pass

    def printBoradWithColor(self, rand_loc, borad):
        for row in range(4):
            print ('-'*39)
            for col in range(4):
                if row == rand_loc[0] and col == rand_loc[1]:
                    print ('\x1b[0;31;40m{0:>5d}{1:>4s}\x1b[0m'.format(borad[row][col], '|')),
                else:
                    print ('{0:>5d}{1:>4s}'.format(borad[row][col], '|')),
            print ''
        print ('-'*39)

    def printBorad(self, action, borad):
        print (action)
        for row in borad:
            print ('-'*39)
            for col in row:
                print ('{0:>5d}{1:>4s}'.format(col, '|')),
            print ''
        print ('-'*39)

class Game(object):
    def __init__(self, borad=None, player=None):
        self.gamePlayer = player
        self.gameBorad = borad
        self.logger = Logger()

    def run(self):
        self.gamePlayer.init_game()
        while not self.gameBorad.isEnd( self.gameBorad.borad ):
            actionName = self.gamePlayer.action()
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

class Borad(object):
    def __init__(self):
        self.actionTable = [ self.moveUp, self.moveDown, self.moveLeft, self.moveRight ]
        self.borad = np.zeros((4,4), dtype=np.int32) 
        self.restore_borad_info()

    def start_FakeGame(self):
        '''
        self.borad = np.zeros((4,4), dtype=np.int32) 
        self.borad[0][0] = 2;
        self.borad[2][0] = 2;
        '''
        # self.borad = np.array( [ [8,2,16,2], [2,1024,1024,8], [8,32,64,2], [0,0,2,0] ] )
        # self.borad = np.array( [ [4,64,512,0], [64,16,4,2], [2,64,256,0], [128,4,2,32] ] )
        # self.borad = np.array( [ [0,8,8,0], [2,4,0,8], [4,2,1024,4], [4,2,1024,2] ] )
        self.borad = np.array( [ [4,64,512,0], [64,16,4,2], [2,64,256,4], [128,4,2,32] ] )
        self.restore_borad_info()

    def startGame(self):
        self.borad = np.zeros((4,4), dtype=np.int32) 
        self.random_blocks( self.borad )
        self.random_blocks( self.borad )
        self.restore_borad_info()

    def save_borad_info(self):
        self.borad = copy.deepcopy(self.simuBorad)

    def restore_borad_info(self):
        self.simuBorad = copy.deepcopy(self.borad)

    def random_blocks(self, temp_borad):
        if not temp_borad.all():
            index = 0
            while True:
                r = random.randint(0,3)
                c = random.randint(0,3)
                if temp_borad[r][c] == 0:
                    temp_borad[r][c] = 2
                    break
        else:
            return 'None'
        return (r,c)

    def isEnd(self, temp_borad):
        if 2048 in temp_borad:
            return True

        for i in range(0,4):
            for j in range(0,4):
                current = temp_borad[i][j]
                if current == 0:
                    return False
                if i > 0 and current == temp_borad[i-1][j]:
                    return False
                if j > 0 and current == temp_borad[i][j-1]:
                    return False
                if i < 3 and current == temp_borad[i+1][j]:
                    return False
                if j < 3 and current == temp_borad[i][j+1]:
                    return False
        else:
            return True 

    def moveUp(self, temp_borad):
        succ_move = False
        origin_borad = copy.deepcopy(temp_borad)
        for c in range(0,4):

            for rs in range(0,4):
                for rz in range(0,3):
                    if temp_borad[rz][c] == 0:
                        temp_borad[rz][c] = temp_borad[rz+1][c]
                        temp_borad[rz+1][c] = 0
            rs = 0
            r = rs + 1
            while rs < 4 and r < 4:
                if temp_borad[rs][c] != 0:
                    if temp_borad[rs][c] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[rs][c] = 0
                        rs = r+1
                        r += 2
                    else:
                        rs = r
                        r += 1
                else:
                    r += 1

            for rs in range(0,4):
                for rz in range(0,3):
                    if temp_borad[rz][c] == 0:
                        temp_borad[rz][c] = temp_borad[rz+1][c]
                        temp_borad[rz+1][c] = 0

        if (origin_borad == temp_borad).all():
            succ_move = False
        else:
            succ_move = True

        return succ_move

    def moveDown(self, temp_borad):
        succ_move = False
        origin_borad = copy.deepcopy(temp_borad)
        for c in range(0,4):

            for rs in range(3,0,-1):
                for rz in range(3,0,-1):
                    if temp_borad[rz][c] == 0:
                        temp_borad[rz][c] = temp_borad[rz-1][c]
                        temp_borad[rz-1][c] = 0
            rs = 3
            r = rs - 1
            while rs > -1 and r > -1:
                if temp_borad[rs][c] != 0:
                    if temp_borad[rs][c] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[rs][c] = 0
                        rs = r-1
                        r -= 2
                    else:
                        rs = r
                        r -= 1
                else:
                    r -= 1

            for rs in range(3,0,-1):
                for rz in range(3,0,-1):
                    if temp_borad[rz][c] == 0:
                        temp_borad[rz][c] = temp_borad[rz-1][c]
                        temp_borad[rz-1][c] = 0

        if (origin_borad == temp_borad).all():
            succ_move = False
        else:
            succ_move = True

        return succ_move

    def moveRight(self, temp_borad):
        succ_move = False
        origin_borad = copy.deepcopy(temp_borad)
        for r in range(0,4):

            for cs in range(3,0,-1):
                for cz in range(3,0,-1):
                    if temp_borad[r][cz] == 0:
                        temp_borad[r][cz] = temp_borad[r][cz-1]
                        temp_borad[r][cz-1] = 0
            cs = 3
            c = cs - 1
            while cs > -1 and c > -1:
                if temp_borad[r][cs] != 0:
                    if temp_borad[r][cs] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[r][cs] = 0
                        cs = c-1
                        c -= 2
                    else:
                        cs = c
                        c -= 1
                else:
                    c -= 1

            for cs in range(3,0,-1):
                for cz in range(3,0,-1):
                    if temp_borad[r][cz] == 0:
                        temp_borad[r][cz] = temp_borad[r][cz-1]
                        temp_borad[r][cz-1] = 0

        if (origin_borad == temp_borad).all():
            succ_move = False
        else:
            succ_move = True

        return succ_move

    def moveLeft(self, temp_borad):
        succ_move = False
        origin_borad = copy.deepcopy(temp_borad)
        for r in range(0,4):

            for cs in range(0,4):
                for cz in range(0,3):
                    if temp_borad[r][cz] == 0:
                        temp_borad[r][cz] = temp_borad[r][cz+1]
                        temp_borad[r][cz+1] = 0
            cs = 0
            c = cs + 1
            while cs < 4 and c < 4:
                if temp_borad[r][cs] != 0:
                    if temp_borad[r][cs] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[r][cs] = 0
                        cs = c+1
                        c += 2
                    else:
                        cs = c
                        c += 1
                else:
                    c += 1

            for cs in range(0,4):
                for cz in range(0,3):
                    if temp_borad[r][cz] == 0:
                        temp_borad[r][cz] = temp_borad[r][cz+1]
                        temp_borad[r][cz+1] = 0

        if (origin_borad == temp_borad).all():
            succ_move = False
        else:
            succ_move = True

        return succ_move

class Player(object):
    def __init__(self, CurrentBorad):
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

# --------------------------------------------------------------------------

class Node(object):
    def __init__(self, parent, borad_2d, action):
        self.parent = parent
        self.borad = copy.deepcopy(borad_2d)
        self.childrens = {}
        self.win = 0
        self.visits = 1
        self.reward = 0
        self.action = action

    def __str__(self):
        return str(self.borad)

    def isFullExpand(self):
        for v in self.childrens.values():
            if v.reward == 0:
                return False
        return True

    def isExpend(self):
        if len(self.childrens) != 0:
            return True
        else:
            return False

    def addChildren(self, node):
        node_id = tuple( map(tuple, node.borad) )
        self.childrens[node_id] = node 

class Monte_Carlo_Player(Player):
    def __init__(self, borad):
        self.gameBorad = borad
        self.root = Node(None, self.gameBorad.borad, None) 
        self.currentNode = None 

    def init_game(self):
        self.gameBorad.startGame()
        # self.gameBorad.start_FakeGame()
        self.currentNode = None

    def action(self):
        if self.currentNode == None:
            self.currentNode = self.root

        key = tuple( map(tuple, self.gameBorad.borad)) 
        if key in self.currentNode.childrens:
            self.currentNode = self.currentNode.childrens[key]
        else:
            newChild = Node(self.currentNode, self.gameBorad.borad, None)
            self.currentNode.childrens[key] = newChild
            self.currentNode = newChild

        self.currentNode = self.uctSearch(self.currentNode)
        self.gameBorad.restore_borad_info()
        self.currentNode.action(self.gameBorad.simuBorad)
        self.currentNode.action(self.gameBorad.borad)
        self.gameBorad.save_borad_info()
        return self.currentNode.action.__name__

    def uctSearch(self, node):
        for i in range(5):
            expandNode = self.treePolicy(node)
            delta = self.defaultPolicy(expandNode)
            self.backpropagation(expandNode, node, delta)

        child = self.bestChild(node)
        return child 

    def treePolicy(self, node):
        v = node
        while not self.gameBorad.isEnd( v.borad ):
            if not v.isExpend():
                self.expand(v)

            if v.isFullExpand():
                v = self.bestChild(v)
            else:
                notExpandNode = [ c for c in v.childrens.values() if c.reward == 0 ]
                return random.choice(notExpandNode)

        return v 

    def expand(self, v):
        for nextAction in self.gameBorad.actionTable:
            simuBorad = copy.deepcopy(v.borad)
            succ_move = nextAction(simuBorad)
            if succ_move:
                n = Node(v, simuBorad, nextAction)
                v.addChildren(n)

        self.gameBorad.restore_borad_info()

    def bestChild(self, node):
        argmax = -1
        argNode = None
        for v in node.childrens.values():
            score = v.reward/v.visits + 1.414*math.sqrt( 2*math.log(node.visits) / v.visits)
            if score > argmax:
                argmax = score
                argNode = v

        return argNode

    def defaultPolicy(self, v):
        reward = 0.0
        simulateTimes = 10 
        if self.gameBorad.isEnd( v.borad ):
            reward = self.getFreeReward(v.borad)
            return reward

        for times in range(simulateTimes):
            depth = 20 # if depth == -1, will go through to game end.
            self.gameBorad.simuBorad = copy.deepcopy(v.borad)
            while depth != 0 and not self.gameBorad.isEnd( self.gameBorad.simuBorad ):
                succ_move = False
                self.gameBorad.random_blocks(self.gameBorad.simuBorad)
                nextAction = self.gameBorad.actionTable[ random.randint(0,3) ]

                if nextAction != None:
                    succ_move = nextAction(self.gameBorad.simuBorad)
                    if succ_move == True:
                        reward += self.getFreeReward(self.gameBorad.simuBorad)
                        depth -= 1

        self.gameBorad.restore_borad_info()
        return reward / simulateTimes

    '''
        Why there are children with same borad???
    '''
    def backpropagation(self, v, node, delta):
        while v != node:
            v.visits += 1
            v.reward += delta
            v = v.parent
        else: # parent node should reflash info
            v.visits += 1
            v.reward += delta

    def getFreeReward(self, borad):
        score = 0
        for i in range(4):
            for j in range(4):
                if borad[i][j] == 2048:
                    score = 999999 
                    return score
                if i-1 >= 0 and borad[i][j] !=0 and borad[i][j] == borad[i-1][j]:
                    # score += borad[i][j]*2
                    score += 1
                if i+1 <= 3 and borad[i][j] !=0 and borad[i][j] == borad[i+1][j]:
                    # score += borad[i][j]*2
                    score += 1
                if j+1 <= 3 and borad[i][j] !=0 and borad[i][j] == borad[i][j+1]:
                    # score += borad[i][j]*2
                    score += 1
                if j-1 >= 0 and borad[i][j] !=0 and borad[i][j] == borad[i][j-1]:
                    # score += borad[i][j]*2
                    score += 1
                #------------------------------------------------------------------
                if i-1 >= 0 and borad[i-1][j] == 0:
                    score += 1
                if i+1 <= 3 and borad[i+1][j] == 0:
                    score += 1
                if j+1 <= 3 and borad[i][j+1] == 0:
                    score += 1
                if j-1 >= 0 and borad[i][j-1] == 0:
                    score += 1
        return score

def unit_test():
    b = Borad()
    m = Monte_Carlo_Player(borad=b)
    g = Game(borad=b, player=m)
    totals = 1 
    wins = 0.0
    for i in range(totals):
        print ('{0} games'.format(i))
        wins += g.run()
    print ('Win rate: ', wins/totals)

def moving_test():
    b = Borad()
    m = Monte_Carlo_Player(borad=b)
    g = Game(b, m)
    g.gamePlayer.init_game()
    print (g.gameBorad.borad)
    print ('-'*5)
    g.gameBorad.moveRight(g.gameBorad.borad)
    print (g.gameBorad.borad)

if __name__ == '__main__':
    cProfile.runctx('unit_test()', globals(), locals())
