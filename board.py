
# Basic Framework
# Game board and tiles

import operator
import shape
from enum import Enum
import copy

Color = Enum('Color', ('BLUE', 'YELLOW', 'RED', 'GREEN', 'PURPLE', 'ORANGE'))
CooDx = [1, 0, -1, 0]
CooDy = [0, 1, 0, -1]
CooDp = [1, 1, -1, -1]
CooDq = [1, -1, -1, 1]

class Coordinate(object):
    def __init__(self, x = 0, y = 0, state = 0):
        self.x = x
        self.y = y
        self.state = state

# class Tiles
class Tiles(object):
    def __init__(self, type = -1, rotation = 0, flip = 0):
        self.type = type
        self.rotation = rotation % 4
        # 0, 1, 2, 3 represent the CLOCKWISE rotation of 0, 90, 180, 270 degrees represently
        self.flip = flip % 2
        # 0: non-flip
        # 1: flip once
        self.shape = [] if type == -1 else shape.shapeSet[type][self.flip * 4 + self.rotation]
        self.corner = [] if type == -1 else shape.cornerSet[type][self.flip * 4 + self.rotation]
        self.size = 0 if type == -1 else len(shape.shapeSet[type][0])
    
    def __rotate(self, deg = 0):
        self.rotation = (self.rotation + deg) % 4
        self.shape = shape.shapeSet[self.type][self.flip * 4 + self.rotation]
        self.corner = shape.cornerSet[self.type][self.flip * 4 + self.rotation]

    def print(self, writeObject = None):
        for i in range(5):
            for j in range(5):
                if (i, j) in self.shape:
                    print("+") if writeObject == None else writeObject.write("+")
                else:
                    print("_") if writeObject == None else writeObject.write("-")
            print("\n") if writeObject == None else writeObject.write("\n")

    def leftRotate(self):
        self.__rotate(3)

    def rightRotate(self):
        self.__rotate(1)

    def horFlip(self):
        # horizontally flip
        self.flip = (self.flip + 1) % 2
        if self.rotation % 2 == 0:
            self.rotation = (self.rotation + 2) % 4
        self.shape = shape.shapeSet[self.type][self.flip * 4 + self.rotation]
        self.corner = shape.cornerSet[self.type][self.flip * 4 + self.rotation]

    def verFlip(self):
        # vertically flip
        self.flip = (self.flip + 1) % 2
        if self.rotation % 2:
            self.rotation = (self.rotation + 2) % 4
        self.shape = shape.shapeSet[self.type][self.flip * 4 + self.rotation] 
        self.corner = shape.cornerSet[self.type][self.flip * 4 + self.rotation]

class Board(object):
    def __init__(self, type = 0, initState = None):
        if initState is None:
            self.type = type
            if type == 0: # Blokus Duo
                self.size = 14
                self.playerNum = 2
                self.color = [1, 2]
                self.tmpColor = [11, 21]
                self.board = [[0 for col in range(14)] for row in range(14)]
                # 0: blank
                # 1: occupied by player 1
                # 2: occupied by player 2
                self.boardState = [[[True for col in range(14)] for row in range(14)] for i in range(self.playerNum)]
                # board state supplementary for players to play tiles
                # True: can be covered (but it may be impossible to be covered)
                # False: cannot be covered (the square has been occupied or is adjacent to the square with the same color)
                self.cornerSets = [set([(4, 4)]), set([(9, 9)])]
                self.tmpSets = [set(), set()]
        elif isinstance(initState, Board):
            self.type = initState.type
            self.size = initState.size
            self.playerNum = initState.playerNum
            self.color = initState.color
            self.board = copy.deepcopy(initState.board)
            self.boardState = copy.deepcopy(initState.boardState)
            self.cornerSets = copy.deepcopy(initState.cornerSets)
            self.tmpSets = copy.deepcopy(initState.tmpSets)
        elif isinstance(initState, dict):
            self.type, self.size, self.playerNum, self.board, self.cornerLists = initState
            self.boardState = [[[True for col in range(14)] for row in range(14)] for i in range(self.playerNum)]
            for i in range(self.size):
                for j in range(self.size):
                    c = self.board[i][j]
                    if c is 0:
                        continue
                    for p in range(self.playerNum):
                        self.boardState[p][i][j] = False
                    player = self.color.index(c)
                    for k in range(4):
                        nx = i + CooDx[k]
                        ny = j + CooDy[k]
                        if self.__isInBound(nx, ny):
                            self.boardState[player][nx][ny] = False
    '''
    def copyBoard(self, newBoard, order):
        if not isinstance(newBoard, Board):
            raise TypeError
        if newBoard.type != self.type:
            raise ValueError
        newBoard.board = copy.deepcopy(self.board)
        newBoard.boardState[order] = copy.deepcopy(self.boardState[order])
        newBoard.cornerSets = copy.copy(self.cornerSets)
    '''

    def __isInBound(self, x, y):
        return (x >= 0 and x < self.size and y >= 0 and y < self.size)

    def isAdj(self, player, x, y):
        for k in range(4):
            nx = x + CooDx[k]
            ny = y + CooDy[k]
            if self.__isInBound(nx, ny):
                if self.board[nx][ny] == self.color[player] or self.board[nx][ny] == self.tmpColor[player]:
                    return True
        return False

    def canDrop(self, player, tile, x, y):
        if not isinstance(tile, Tiles):
            raise TypeError
        if tile.type == -1:
            raise ValueError
        coverCorner = False
        for coo in tile.shape:
            if not self.__isInBound(x + coo[0], y + coo[1]):
                return False
            if not self.boardState[player][x + coo[0]][y + coo[1]]:
                return False
            if not self.cornerSets[player].isdisjoint(set([(x + coo[0], y + coo[1])])):
                coverCorner = True
        return coverCorner

    def dropTile(self, player, tile, x, y):
        if not isinstance(tile, Tiles):
            raise TypeError
        if tile.type == -1:
            raise ValueError
        if player < 0 or player >= self.playerNum:
            raise ValueError
        if not self.canDrop(player, tile, x, y):
            return False
        for i in range(self.playerNum):
            for coo in tile.shape:
                self.boardState[i][coo[0] + x][coo[1] + y] = False
        for coo in tile.shape:
            for k in range(4):
                nx = x + coo[0] + CooDx[k]
                ny = y + coo[1] + CooDy[k]
                if self.__isInBound(nx, ny):
                    self.boardState[player][nx][ny] = False
            self.board[x + coo[0]][y + coo[1]] = self.color[player]
        for coo in tile.corner:
            if self.__isInBound(x + coo[0], y + coo[1]):
                self.cornerSets[player].update([(x + coo[0], y + coo[1])])
        return True

    def tryDrop(self, player, tile, x, y):
        if not isinstance(tile, Tiles):
            raise TypeError
        if tile.type == -1:
            raise ValueError
        if player < 0 or player >= self.playerNum:
            raise ValueError
        if not self.canDrop(player, tile, x, y):
            return False
        for coo in tile.shape:
            self.board[x + coo[0]][y + coo[1]] = self.tmpColor[player]
        for coo in tile.corner:
            if self.__isInBound(x + coo[0], y + coo[1]):
                self.tmpSets[player].update([(x + coo[0], y + coo[1])])
        self.tmpSets[player] = self.tmpSets[player] - self.cornerSets[player]
        return True

    def retraceDrop(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.tmpColor[player]:
                    self.board[i][j] = 0
        self.tmpSets[player] = set()
    
    def print(self, fout):
        for i in range(self.size):
            for j in range(self.size):
                fout.write(chr(shape.colorAscii[self.board[i][j]]))
                fout.write(chr(32))
            fout.write("\n")
        fout.write("\n")

    def getInfo(self):
        return {
            "boardType" : self.type,
            "boardSize" : self.size,
            "playerNum" : self.playerNum,
            "board" : self.board,
            "cornerSets" : self.cornerSets
        }
