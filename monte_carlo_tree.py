import math
import copy
import random
import numpy as np

class Game(object):
    def __init__(self, borad=None, player=None):
        self.gamePlayer = player
        self.gameBorad = borad

    def run(self):
        self.gameBorad.startGame()
        while not self.gameBorad.isEnd( self.gameBorad.borad ):
            self.gamePlayer.action()
            self.gameBorad.random_blocks(self.gameBorad.borad)
            print self.gameBorad.borad
            print '-'*30
        else:
            print 'Game finish'
            print self.gameBorad.borad

class Borad(object):
    def __init__(self):
        self.actionTable = [ self.moveUp, self.moveDown, self.moveLeft, self.moveLeft ]
        self.borad = np.zeros((4,4), dtype=np.int32) 
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

    def isEnd(self, temp_borad):
        if 2048 in temp_borad:
            print 'Player win'
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
        for c in range(0,4):
            rs = 0
            r = rs + 1
            while rs < 4 and r < 4:
                if temp_borad[r][c] != 0:
                    if temp_borad[rs][c] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[rs][c] = 0
                        rs = r+1
                        r += 2
                        succ_move = True
                    else:
                        rs = r
                        r += 1
                else:
                    r += 1
                    succ_move = True

            for rs in range(0,4):
                for rz in range(0,3):
                    if temp_borad[rz][c] == 0:
                        temp_borad[rz][c] = temp_borad[rz+1][c]
                        temp_borad[rz+1][c] = 0
        return succ_move

    def moveDown(self, temp_borad):
        succ_move = False
        for c in range(0,4):
            rs = 3
            r = rs - 1
            while rs > -1 and r > -1:
                if temp_borad[r][c] != 0:
                    if temp_borad[rs][c] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[rs][c] = 0
                        rs = r-1
                        r -= 2
                        succ_move = True
                    else:
                        rs = r
                        r -= 1
                else:
                    r -= 1
                    succ_move = True

            for rs in range(3,0,-1):
                for rz in range(3,0,-1):
                    if temp_borad[rz][c] == 0:
                        temp_borad[rz][c] = temp_borad[rz-1][c]
                        temp_borad[rz-1][c] = 0

        return succ_move

    def moveRight(self, temp_borad):
        succ_move = False
        for r in range(0,4):
            cs = 3
            c = cs - 1
            while cs > -1 and c > -1:
                if temp_borad[r][c] != 0:
                    if temp_borad[r][cs] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[r][cs] = 0
                        cs = c-1
                        c -= 2
                        succ_move = True
                    else:
                        cs = c
                        c -= 1
                else:
                    c -= 1
                    succ_move = True

            for cs in range(3,0,-1):
                for cz in range(3,0,-1):
                    if temp_borad[r][cz] == 0:
                        temp_borad[r][cz] = temp_borad[r][cz-1]
                        temp_borad[r][cz-1] = 0

        return succ_move

    def moveLeft(self, temp_borad):
        succ_move = False
        for r in range(0,4):
            cs = 0
            c = cs + 1
            while cs < 4 and c < 4:
                if temp_borad[r][c] != 0:
                    if temp_borad[r][cs] == temp_borad[r][c]:
                        temp_borad[r][c] *= 2
                        temp_borad[r][cs] = 0
                        cs = c+1
                        c += 2
                        succ_move = True
                    else:
                        cs = c
                        c += 1
                else:
                    c += 1
                    succ_move = True

            for cs in range(0,4):
                for cz in range(0,3):
                    if temp_borad[r][cz] == 0:
                        temp_borad[r][cz] = temp_borad[r][cz+1]
                        temp_borad[r][cz+1] = 0

        return succ_move

class Player(object):
    def __init__(self, CurrentBorad):
        self.gameBorad = borad
        print 'Player init'

    def random_action(self):
        succ_move = False
        while not succ_move:
            self.gameBorad.restore_borad_info()
            nextAction = self.gameBorad.actionTable[ random.randint(0,3) ]
            succ_move = nextAction(self.gameBorad.simuBorad)

        nextAction(self.gameBorad.borad)
        self.gameBorad.save_borad_info()

    def action(self):
        print 'Player run'
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
        self.root = None 
        self.currentNode = None 

    def action(self):
        if self.currentNode == None:
            self.root = Node(None, self.gameBorad.borad, None)
            self.currentNode = copy.deepcopy(self.root)

        self.currentNode = self.uctSearch(self.currentNode)

        self.gameBorad.restore_borad_info()

        nextAction = self.currentNode.action
        nextAction(self.gameBorad.simuBorad)
        nextAction(self.gameBorad.borad)

        self.gameBorad.save_borad_info()

    def uctSearch(self, node):
        for i in range(2):
            vl = copy.deepcopy(node)
            vl = self.treePolicy(node)
            delta = self.defaultPolicy()
            self.backpropagation(vl, delta)

        return self.bestChild(vl) 

    def treePolicy(self, node):
        v = copy.deepcopy(node)
        while not self.gameBorad.isEnd( v.borad ):
            if v.isExpend():
                '''
                    Why not to here?
                '''
                print 'v.isExpend'
                v = self.bestChild(v)
            else:
                self.expand(v)
                return v

        return v 

    def expand(self, v):
        for nextAction in self.gameBorad.actionTable:
            self.gameBorad.restore_borad_info()
            succ_move = nextAction(self.gameBorad.simuBorad)
            if succ_move:
                n = Node(v, self.gameBorad.simuBorad, nextAction)
                v.addChildren(n)

        self.gameBorad.restore_borad_info()

    def bestChild(self, node):
        argmax = -1
        argNode = None
        for v in node.childrens.values():
            score = v.reward/v.visits + 2*math.sqrt( 2*math.log(node.visits) / v.visits)
            print score
            if score > argmax:
                argNode = v

        return argNode

    def defaultPolicy(self):
        reward = 0
        while not self.gameBorad.isEnd( self.gameBorad.simuBorad ):
            succ_move = False
            self.gameBorad.random_blocks(self.gameBorad.simuBorad)
            nextAction = self.gameBorad.actionTable[ random.randint(0,3) ]
            succ_move = nextAction(self.gameBorad.simuBorad)

            if succ_move == True:
                reward += getFreeScore(self.gameBorad.simuBorad)
        else:
            pass
            '''
            print '='*30
            print 'end simuBorad'
            print self.gameBorad.simuBorad
            print '='*30
            '''

        return reward

    def backpropagation(self, v, delta):
        while v is not None:
            v.visits += 1
            v.reward += delta
            v = v.parent

def getFreeScore(borad):
    maxValue = 0
    score = 0
    for i in range(0,4):
        for j in range(0,4):
            if borad[i][j] == 2048:
                score = 9999999
                return score
            if i-1 >= 0 and borad[i][j] != 0 and borad[i][j] == borad[i-1][j]:
                score += borad[i][j]*2
            if i-1 >= 0 and borad[i-1][j] == 0:
                score += 1 
            if j+1 <= 3 and borad[i][j] != 0 and borad[i][j] == borad[i][j+1]:
                score += borad[i][j]*2
            if j+1 <= 3 and borad[i][j+1] == 0:
                score += 1 
            if i+1 <= 3 and borad[i][j] != 0 and borad[i][j] == borad[i+1][j]:
                score += borad[i][j]*2
            if i+1 <= 3 and borad[i+1][j] == 0:
                score += 1 
            if j-1 >= 0 and borad[i][j] != 0 and borad[i][j] == borad[i][j-1]:
                score += borad[i][j]*2
            if j-1 >= 0 and borad[i][j-1] == 0:
                score += 1 

    return score

def unit_test():
    b = Borad()
    m = Monte_Carlo_Player(b)
    g = Game(b, m)
    g.run()

if __name__ == '__main__':
    unit_test()
