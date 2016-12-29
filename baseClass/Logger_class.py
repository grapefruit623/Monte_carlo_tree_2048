# -*- codgin: utf-8 -*-

class Logger(object):
    def __init__(self):
        pass

    def printBoradWithColor(self, rand_loc, borad):
        for row in range(4):
            print ('-'*39)
            for col in range(4):
                if row == rand_loc[0] and col == rand_loc[1]:
                    print ('\x1b[0;31;40m{0:>5d}{1:>4s}\x1b[0m'.format(borad[row][col], '|'), end=""),
                else:
                    print ('{0:>5d}{1:>4s}'.format(borad[row][col], '|'), end="")
            print ('')
        print ('-'*39)

    def printBorad(self, action, borad):
        print (action)
        for row in borad:
            print ('-'*39)
            for col in row:
                print ('{0:>5d}{1:>4s}'.format(col, '|'), end="")
            print ('')
        print ('-'*39)

    '''
        Should I modifies this function to async func?
    '''
    def recordBorad_and_Action(self, borad, actionName):
        with open('borad_record.txt', 'a') as f:
            f.write('{0}:{1}\n'.format(actionName, ' '.join(str(x) for x in borad.flatten())))

