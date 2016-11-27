# -*- codgin: utf-8 -*-
import numpy as np
import copy
import random

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
