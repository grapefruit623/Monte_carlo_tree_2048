import numpy as np
import tkinter as tk
from tkinter import font

class GuiBorad(object):
    def __init__(self):
        self.numLocs = [ (45,45), (150,45), (250,45), (350,45),
                         (45,150), (150,150), (250,150), (350,150),
                         (45,250), (150,250), (250,250), (350,250),
                         (45,350), (150,350), (250,350), (350,350) ]

    def drawNewBoard(self):
        self.canvas = tk.Canvas(self, bg='white', width=400, height=400)
        self.canvas.grid(row=0, column=0)

        for loc in (100, 200, 300):
            self.canvas.create_line((0, loc), (400, loc), dash=(5,))
            self.canvas.create_line((loc, 0), (loc, 400), dash=(5,))

    def drawGamingBoard(self, board):
        testNum = self.canvas.create_text(45, 45, text=5, font=font.Font(size=30, weight='bold'))
        testNum = self.canvas.create_text(150, 45, text=1024, font=font.Font(size=30, weight='bold'))
        testNum = self.canvas.create_text(250, 45, text=1024, font=font.Font(size=30, weight='bold'))
        testNum = self.canvas.create_text(350, 45, text=1024, font=font.Font(size=30, weight='bold'))
        testNum = self.canvas.create_text(150, 350, text=256, font=font.Font(size=30, weight='bold'))
        testNum = self.canvas.create_text(350, 350, text=256, font=font.Font(size=30, weight='bold'))

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        print (id(tk))
        self.createWidget()
        self.gameBoard = GuiBorad()
        self.gameBoard.drawNewBoard()

        self.pack()

    def say_hi(self):
        print ('hi')

    def createWidget(self):
        self.QUIT = tk.Button(self)
        self.QUIT['text'] = 'QUIT'
        self.QUIT['fg'] = 'red'
        self.QUIT['command'] = self.quit
        self.QUIT.grid(row=0, column=1)

        self.hi_there = tk.Button(self)
        self.hi_there['text'] = 'hello'
        self.hi_there['command'] = self.say_hi
        self.hi_there.grid(row=1, column=1)

        self.label = tk.Label(self, text='Label', fg='black', bg='blue', width=30, height=2)
        self.label.grid(row=2, column=1)




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
