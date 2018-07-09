
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
        self.maxRotation = 0 if type == -1 else shape.tileMaxRotation[type]
        self.rotation = rotation % max(self.maxRotation, 1)
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
                self.board = [[0 for col in range(14)] for row in range(14)]
                # 0: blank
                # 1: occupied by player 1
                # 2: occupied by player 2
        elif isinstance(initState, Board):
            self.type = initState.type
            self.size = initState.size
            self.playerNum = initState.playerNum
            self.color = initState.color
            self.board = copy.deepcopy(initState.board)
        elif isinstance(initState, dict):
            self.type, self.size, self.playerNum, self.board = initState
            self.color = [i + 1 for i in range(self.playerNum)]

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

    def isInBound(self, x, y):
        return (x >= 0 and x < self.size and y >= 0 and y < self.size)

    def isAdj(self, player, x, y):
        for k in range(4):
            nx = x + CooDx[k]
            ny = y + CooDy[k]
            if self.isInBound(nx, ny):
                if self.board[nx][ny] == self.color[player]:
                    return True
        return False

    def isCorner(self, player, x, y):
        for k in range(4):
            nx = x + CooDp[k]
            ny = y + CooDq[k]
            if self.isInBound(nx, ny):
                if self.board[nx][ny] == self.color[player]:
                    return True
        return False

    def getCorners(self, player):
        ret = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and not self.isAdj(player, i, j) and self.isCorner(player, i, j):
                    ret.update([i, j])
        return ret

    def canDrop(self, player, tile, x, y):
        if not isinstance(tile, Tiles):
            raise TypeError
        if tile.type == -1:
            raise ValueError
        coverCorner = False
        for coo in tile.shape:
            if not self.isInBound(x + coo[0], y + coo[1]):
                return False
            if self.board[x + coo[0]][y + coo[1]] != 0:
                return False
            if self.isAdj(player, x + coo[0], y + coo[1]):
                return False
            if self.isCorner(player, x + coo[0], y + coo[1]) \
            or (x + coo[0], y + coo[1]) == (4, 4) \
            or (x + coo[0], y + coo[1]) == (9, 9):
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
        for coo in tile.shape:
            self.board[x + coo[0]][y + coo[1]] = self.color[player]
        return True
    '''
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
            self.board[x + coo[0]][y + coo[1]] = self.Color[player]
        return True
    '''
    '''
    def retraceDrop(self, pointList):
        for coo in pointList:
            self.board[coo[0]][coo[1]] = 0
    '''

    def retraceDrop(self, tile, x, y):
        for coo in tile.shape:
            self.board[x + coo[0]][y + coo[1]] = 0

    def print(self, fout = None):
        for i in range(self.size):
            for j in range(self.size):
                if fout is None:
                    print("%d " % self.board[i][j], end = '')
                else:
                    fout.write(chr(shape.colorAscii[self.board[i][j]]))
                    fout.write(chr(32))
            print() if fout is None else fout.write("\n")

    def getScore(self):
        scores = [0 for i in range(self.playerNum)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    scores[self.board[i][j] - 1] = scores[self.board[i][j] - 1] + 1
        return scores

    def getInfo(self):
        return {
            "boardType" : self.type,
            "boardSize" : self.size,
            "playerNum" : self.playerNum,
            "board" : self.board,
        }

    def parseFromMatrix(self, matrix, player):
        self.type = 0
        self.size = 14
        self.playerNum = 2
        self.color = [1, 2]
        self.board = copy.deepcopy(matrix)
        visited = [[False for i in range(14)] for j in range(14)]

        def getTile(x, y, color, tilePoints, minx, miny):
            visited[x][y] = True
            tilePoints.append((x, y))
            for k in range(4):
                nx = x + CooDx[k]
                ny = y + CooDy[k]
                if self.isInBound(nx, ny):
                    if matrix[nx][ny] == color and not visited[nx][ny]:
                        minx = min(minx, nx)
                        miny = min(miny, ny)
                        getTile(nx, ny, color, tilePoints, minx, miny)

        for i in range(14):
            for j in range(14):
                if matrix[i][j] != 0 and not visited[i][j]:
                    tilePoints = []
                    minx = 14
                    miny = 14
                    getTile(i, j, matrix[i][j], tilePoints, minx, miny)
                    for i in range(len(tilePoints)):
                        tilePoints[i][0] = tilePoints[i][0] - minx
                        tilePoints[i][1] = tilePoints[i][1] - miny
                    tilePoints.sort()
                    for t in range(21):
                        if shape.tileSizes[t] != len(tilePoints):
                            continue
                        if tilePoints in shape.shapeSet[t]:
                            player[matrix[i][j]].used[t] = True
                            player[matrix[i][j]].scores += shape.tileSizes[t]
                            break

