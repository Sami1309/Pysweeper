import random

class MineSweeper(object):

    

    def __init__(self, height, width, bombs):

        self.height = height
        self.width = width
        self.bombs = bombs
        self.totalBombs = self.bombs
        self.gameLost = False

        # 2D array of 2 index lists
        #first index is the number of adjacent bombs, 0 for none up to 8. -1 if it is a bomb
        #second index is if it is currently uncovered, 0 for covered, 1 for uncovered, 2 for flagged
        self.board = [[[0, 0] for _ in range(self.width)] for _ in range(self.height)]

        self.populateBombs()
        self.generateAdjacencies()

    def populateBombs(self):

        for b in range(self.bombs):

            bombPos = (random.randrange(self.height), random.randrange(self.width))
            while self.board[bombPos[0]][bombPos[1]][0] == -1:
                bombPos = (random.randrange(self.height), random.randrange(self.width))
            self.board[bombPos[0]][bombPos[1]][0] = -1
    
    def generateAdjacencies(self):
        
        for i in range(self.height):
            for j in range(self.width):
                bombCount = 0
                for m in range(-1,2):
                    for n in range(-1,2):
                        if 0 <= i+m < self.height and 0 <= j+n < self.width:
                            if self.board[i+m][j+n][0] == -1:
                                bombCount += 1
                if self.board[i][j][0] != -1:
                    self.board[i][j][0] = bombCount
    
    def getGameData(self):
        height = int(input("Board height: "))
        width = int(input("Board width: " ))
        bombs = int(input("Number of bombs: "))

        return height, width, bombs

    def displayInstructions(self):
        print("""
            ---Welcome to MineSweeper---
        The object of the game is to find all the mines
        by either flagging every one or digging every safe
        square.
        """)

    def displayBoard(self):
        boardStr = ''

        for i in range(self.height):
            boardStr += '|'
            for j in range(self.width):
                if self.gameLost and self.board[i][j][0] == -1:
                    boardStr += 'X|'
                elif self.board[i][j][1] == 2:
                    boardStr += 'F|'
                elif self.board[i][j][1] == 0:
                    boardStr += '_|'
                else:
                    boardStr += str(self.board[i][j][0]) + '|'
            boardStr += '\n'
        print(boardStr)
    
    def getMoveInputs(self):

        flagSelect = False
        flag = input('Flag or dig?: ')
        row = int(input('Select row: '))
        col = int(input('Select col: '))
        if flag == 'f':
            flagSelect = True
        return flagSelect, row, col

    #This method reveals every adjacent and subsequently adjacent non bomb-facing square
    #To be triggered whenever a non-bomb adjacent square is clicked
    def unravelBoard(self, row, col):
        selectStack = [(row,col)]
        returnList = []
        while selectStack:
            (i, j) = selectStack.pop()
            #print(i, j)
            self.board[i][j][1] = 1
            for m in range(-1,2):
                for n in range(-1,2):
                    if 0 <= i+m < self.height and 0 <= j+n < self.width and self.board[i+m][j+n][0] == 0 and self.board[i+m][j+n][1] == 0 and not (m == n == 0):
                        selectStack.append((i+m,j+n))
                        returnList.append((i+m,j+n, str(self.board[i+m][j+n][0])))
                    elif 0 <= i+m < self.height and 0 <= j+n < self.width and self.board[i+m][j+n] != -1 and not (m == n == 0) and self.board[i+m][j+n][1] == 0: 
                        self.board[i+m][j+n][1] = 1
                        returnList.append((i+m,j+n, str(self.board[i+m][j+n][0])))
                        
        
        return returnList

    def processFlag(self, row, col):
        if self.board[row][col][1] == 2:
            if self.board[row][col][0] == -1:
                self.totalBombs += 1
            self.board[row][col][1] = 0
        else:
            self.board[row][col][1] = 2
            if self.board[row][col][0] == -1:
                self.totalBombs -= 1
            print(self.totalBombs)
            if self.totalBombs == 0:
                return 1
        return 0

    def processInput(self,row,col):
        changeList = []
        if self.board[row][col][0] == -1:
            changeList.append((row,col,'bomb'))
            self.gameLost = True
            return changeList
        self.board[row][col][1] = 1
        changeList.append((row,col,str(self.board[row][col][0])))
        if self.board[row][col][0] == 0:
            changeList.extend(self.unravelBoard(row,col))
        return changeList
    def processPlayerMove(self):
        flag, row, col = self.getMoveInputs()

        if flag:
            self.board[row][col][1] = 2
            return False
        if self.board[row][col][0] == -1:
            self.board[row][col][1] = 1
            self.gameLost = True
            return True        
        self.board[row][col][1] = 1
        if self.board[row][col][0] == 0:
            lister = self.unravelBoard(row,col)
    
    def displayClosingScreen(self):

        self.displayBoard()
        if self.gameLost:
            print("""
                ---You Lost the Game---
            Better luck next time!
            """
            )
            return None
        print("""
            ---You Won! Congratulations!---
            """)

    def playGame(self):
        self.displayInstructions()

        gameOver = False

        while not gameOver:
            self.displayBoard()
            gameOver = self.processPlayerMove()
        
        self.displayClosingScreen()
if __name__ == '__main__':

    ms = MineSweeper()
    ms.playGame()


