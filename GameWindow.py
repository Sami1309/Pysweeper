#!/usr/bin/python

import tkinter as tk
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Label, Style
import MineSweeper as ms
from PIL import Image
import os

class BoardTile(object):
    def __init__(self, app, frame: tk.Frame,row: int,col: int,flagged: bool,bomb: bool,adj: int):
        
        self.app = app
        self.image = tk.PhotoImage(file=app.graphics['facingDown'])
        self.button = tk.Button(frame, text='', image=self.image,command=lambda pos=(row,col): app.selectSquare(pos), compound="c")
        self.button.bind('<Button-3>', app.selectFlag)
        self.button.grid(row=row,column=col)
        self.row = row #which row
        self.col = col #which column
        self.flagged = flagged #flagged or not
        self.bomb = bomb #bomb present or not
        self.adj = adj #number of adjacent bombs
        self.dug = False
    
    def select(self):
        graphic = str(self.adj)
        if self.bomb:
            graphic = 'bomb'
        self.image = tk.PhotoImage(file=self.app.graphics[graphic])
        self.button['image'] = self.image
        self.button['state'] = tk.DISABLED
        self.dug = True

    def selectFlag(self):
        if not self.dug:
            if not self.flagged:
                self.image = tk.PhotoImage(file=self.app.graphics['flagged'])
                self.button['image'] = self.image
                self.button['state'] = tk.DISABLED
                self.flagged = True
                winCondition = self.app.minesweeper.processFlag(self.row,self.col)
                return winCondition
            else:
                self.image = tk.PhotoImage(file=self.app.graphics['facingDown'])
                self.button['image'] = self.image
                self.flagged = False
                self.button['state'] = tk.NORMAL
                winCondition = self.app.minesweeper.processFlag(self.row,self.col)
                return winCondition
        


class Application(Frame):
    def __init__(self, root):
        self.master = root
        #Format for initilization is height, width, bombs
        self.minesweeper = ms.MineSweeper(15, 15, 10)
        self.resizeImages(30)
        self.graphics = self.getGraphics()
        self.renderMenu()
        self.renderBoard()
        
        #self.master.mainloop()


        
    def resizeImages(self,dimensions):
        f = './MSgraphics'
        for file in os.listdir(f):
            f_img = f+'/'+file
            img=Image.open(f_img)
            img = img.resize((dimensions,dimensions), Image.NEAREST)
            img.save(f_img)
    
    def getGraphics(self):
        graphicsDirectory = "./MSgraphics"
        graphicsList = {}
        for filename in os.listdir(graphicsDirectory):
            fileTitle = filename.split('.')[0]
            graphicsList[fileTitle] = graphicsDirectory + '/' + filename
        return graphicsList

    def renderMenu(self):
        self.master.geometry("800x800")
        self.master.title("MineSweeper")
        variable = tk.StringVar(self.master)
        variable.set('one')

        w = tk.OptionMenu(self.master, variable, 'one','two','three')
        #w.pack()

    def renderBoard(self):


        width, height, = self.minesweeper.width, self.minesweeper.height
        #self.mineButtons = [[{} for _ in range(width)] for _ in range(height)]
        self.boardTile = [[None for _ in range(width)] for _ in range(height)]
        for h in range(height):
            for w in range(width):

                self.boardTile[h][w] = BoardTile(self, self.master, h, w, False, self.minesweeper.getBomb(h,w), self.minesweeper.getTileContents(h,w))
                

    def gameOver(self):
        #A bomb has been selected
        print("game over")
    def selectSquare(self,square):

        h,w = square[0],square[1]
        boardChanges = self.minesweeper.processInput(h,w)

        for b in boardChanges:

            row = b[0]
            col = b[1]
            image = b[2]
            self.boardTile[row][col].select()

            if image == 'bomb':
                self.gameOver()
                return None


    def winGame(self):
        print("You won the game!")
    
    def selectFlag(self, square):

        button = str(square.widget).split('button')[1]

        if button == '':
            buttonNum = 0
        else:
            buttonNum = int(button)-1
        
        row = buttonNum//self.minesweeper.width
        col = buttonNum%self.minesweeper.width

        winCondition = self.boardTile[row][col].selectFlag()
        if winCondition:
            self.winGame()

        


def main():
    root = Tk()
    app = Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()