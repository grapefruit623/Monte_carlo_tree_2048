import numpy as np
import tkinter as tk
from tkinter import font
import threading
import time
import queue

'''
    Should be widget 
'''
class Board(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.numLocs = [ (45,45), (150,45), (250,45), (350,45),
                         (45,150), (150,150), (250,150), (350,150),
                         (45,250), (150,250), (250,250), (350,250),
                         (45,350), (150,350), (250,350), (350,350) ]
        self.canvas = tk.Canvas(self, bg='white', width=400, height=400)
        self.canvas.grid(row=0, column=0)
        self.drawBoardLine()
        self.drawGamingBoard(board=np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]] ))
        self.pack()

    def drawBoardLine(self):
        self.canvas.create_rectangle(0, 0, 400, 400, fill='white')
        for loc in (100, 200, 300):
            self.canvas.create_line((0, loc), (400, loc), dash=(5,))
            self.canvas.create_line((loc, 0), (loc, 400), dash=(5,))

        # self.canvas.create_rectangle(10,10,90,90, fill='red' )

    def drawGamingBoard(self, board=None):
        self.drawBoardLine()
        board = board.flatten()
        for i in range(len(board)):
            self.canvas.create_text(self.numLocs[i], text=board[i], font=font.Font(size=30, weight='bold'))

class mainFrame(tk.Frame):
    def __init__(self, master=None, dataQueue=None, gameCtrl=None):
        print ('mainFrame init: ', threading.get_ident())
        tk.Frame.__init__(self, master)
        self.master = master
        self.gameCtrl = gameCtrl
        self.dataQueue = dataQueue
        self.gameBoard = Board()
        self.createWidget()
        self.pollData()

    def pollData(self):
        if self.dataQueue.empty():
            self.master.after(100, self.pollData)
            return 

        data = self.dataQueue.get()
        self.gameBoard.drawGamingBoard(data['board'])
        self.highScore.set('score: {0}'.format(data['board'].max()))
        self.moveAct.set('action: {0}'.format(data['action']))
        self.master.after(100, self.pollData)

    def createWidget(self):
        print ('createWidget: ', threading.get_ident())
        self.QUIT = tk.Button(self)
        self.QUIT['text'] = 'QUIT'
        self.QUIT['fg'] = 'red'
        self.QUIT['command'] = self.quit
        self.QUIT.grid(row=0, column=1)

        self.start = tk.Button(self)
        self.start['text'] = 'start'
        self.start['command'] = self.gameStart
        self.start.grid(row=2, column=1)

        self.highScore = tk.StringVar()
        self.highScore.set('0')
        self.scoreLabel = tk.Label(self, textvariable=self.highScore, fg='black', bg='white', width=30, height=2)
        self.scoreLabel.grid(row=0, column=2)

        self.moveAct = tk.StringVar()
        self.moveAct.set('High')
        self.movelabel = tk.Label(self, textvariable=self.moveAct, fg='black', bg='white', width=30, height=2)
        self.movelabel.grid(row=1, column=2)

        self.pack()

    def gameStart(self):
        print ('start: {0}'.format(threading.get_ident()))
        self.gameCtrl.start()

class GuiThread(threading.Thread):
    def __init__(self, gameCtrl=None):
        super().__init__()
        print ('Gui thread init', threading.get_ident())
        self.dataQueue = queue.Queue()
        gameCtrl.dataQueue = self.dataQueue
        self.fakeGame = gameCtrl

    def run(self):
        print ('Gui thread run', threading.get_ident())
        print ('GuiThread run start')
        self.root = tk.Tk()
        self.app = mainFrame(master=self.root, dataQueue=self.dataQueue, gameCtrl=self.fakeGame)
        self.app.mainloop()
        print ('GuiThread run end')

class FakeGame(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        print ('FakeGame: ', threading.get_ident())
        b = np.random.randint(low=0, high=2048, size=(4,4))
        self.fakeGameFlow()

    def fakeGameFlow(self):
        for i in range(10000):
            b = np.random.randint(low=0, high=2048, size=(4,4))
            print (b)
            self.dataQueue.put({'board':b, 'action':'up'})

if __name__ == '__main__':
    print ('main', threading.get_ident())
    fg = FakeGame()
    g = GuiThread(gameCtrl=fg)
    g.start()

