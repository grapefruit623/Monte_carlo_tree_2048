import math
import copy
import random
import numpy as np

from baseClass.Player_class import Player

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

# --------------------------------------------------------------------------

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

        bestChild = self.uctSearch(self.currentNode)
        self.currentNode.action = bestChild.action # Record current borad with chosen action
        self.currentNode = bestChild
        self.gameBorad.restore_borad_info()
        bestChild.action(self.gameBorad.simuBorad)
        bestChild.action(self.gameBorad.borad)
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
                '''
                if borad[i][j] == 2048:
                    score = 999999 
                    return score
                '''
                if i-1 >= 0 and borad[i][j] !=0 and borad[i][j] == borad[i-1][j]:
                    score += borad[i][j]*2
                    # score += 1
                if i+1 <= 3 and borad[i][j] !=0 and borad[i][j] == borad[i+1][j]:
                    score += borad[i][j]*2
                    # score += 1
                if j+1 <= 3 and borad[i][j] !=0 and borad[i][j] == borad[i][j+1]:
                    score += borad[i][j]*2
                    # score += 1
                if j-1 >= 0 and borad[i][j] !=0 and borad[i][j] == borad[i][j-1]:
                    score += borad[i][j]*2
                    # score += 1
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
