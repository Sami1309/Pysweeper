#!/usr/bin/python

import tkinter as tk
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Label, Style
import MineSweeper as ms
from PIL import Image
import os

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
        self.mineButtons = [[{} for _ in range(width)] for _ in range(height)]

        
        for h in range(height):
            for w in range(width):
                self.mineButtons[h][w]['image'] =  tk.PhotoImage(file=self.graphics['facingDown'])
                self.mineButtons[h][w]['button'] = tk.Button(self.master, text='', image=self.mineButtons[h][w]['image'],command=lambda pos=(h,w): self.selectSquare(pos), compound="c")
                self.mineButtons[h][w]['button'].bind('<Button-3>', self.selectFlag)
                self.mineButtons[h][w]['flagged'] = False
                self.mineButtons[h][w]['button'].grid(row=h,column=w)

    def gameOver(self):
        #A bomb has been selected
        print("game over")
    def selectSquare(self,square):
        h,w = square[0],square[1]
        boardChanges = self.minesweeper.processInput(h,w)
        #self.mineButtons[h][w]['image'] = tk.PhotoImage(file=self.graphics['0'])
        #self.mineButtons[h][w]['button']['image'] = self.mineButtons[h][w]['image']
        #print(boardChanges)
        for b in boardChanges:
            #print(b)
            row = b[0]
            col = b[1]
            image = b[2]
            #print(row,col,image)
            self.mineButtons[row][col]['image'] = tk.PhotoImage(file=self.graphics[image])
            self.mineButtons[row][col]['button']['image'] = self.mineButtons[row][col]['image']
            self.mineButtons[row][col]['button']['state'] = tk.DISABLED
            if image == 'bomb':
                self.gameOver()
                return None

    def doNothing(self):
        print('')

    def winGame(self):
        print("You won the game!")
    def selectFlag(self, square):
        h,w = 0,0
        #print(square.widget)
        button = str(square.widget).split('button')[1]
        if button == '':
            buttonNum = 0
        else:
            buttonNum = int(button)-1
        h = buttonNum//self.minesweeper.width
        w = buttonNum%self.minesweeper.width
        #print(self.mineButtons[h][w]['flagged'])
        #print(h,w)
        if self.mineButtons[h][w]['flagged'] == False and self.mineButtons[h][w]['button']['state'] == tk.DISABLED:
            return None
        if self.mineButtons[h][w]['flagged'] == False:
            self.mineButtons[h][w]['image'] = tk.PhotoImage(file=self.graphics['flagged'])
            self.mineButtons[h][w]['button']['image'] = self.mineButtons[h][w]['image']
            self.mineButtons[h][w]['flagged'] = True
            self.mineButtons[h][w]['button']['command'] = None
            self.mineButtons[h][w]['button']['state'] = tk.DISABLED
            winCondition = self.minesweeper.processFlag(h,w)
            if winCondition == 1:
                self.winGame()
                return None
        else:
            self.mineButtons[h][w]['image'] = tk.PhotoImage(file=self.graphics['facingDown'])
            self.mineButtons[h][w]['button']['image'] = self.mineButtons[h][w]['image']
            self.mineButtons[h][w]['flagged'] = False
            self.mineButtons[h][w]['button']['command'] = lambda pos=(h,w): self.selectSquare(pos)
            self.mineButtons[h][w]['button']['state'] = tk.NORMAL
            winCondition = self.minesweeper.processFlag(h,w)


def main():
    root = Tk()
    app = Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()