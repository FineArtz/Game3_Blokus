
# Basic Framework
# Game board and tiles

import operator
import shape
from enum import Enum
import copy
import numpy as np 

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
                    print("+") if writeObject is None else writeObject.write("+")
                else:
                    print("_") if writeObject is None else writeObject.write("-")
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
                self.board = np.zeros((14, 14), dtype = int)
                # 0: blank
                # 1: occupied by player 1
                # 2: occupied by player 2
        elif isinstance(initState, Board):
            self.type = initState.type
            self.size = initState.size
            self.playerNum = initState.playerNum
            self.color = initState.color
            self.board = initState.board.copy()
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
        if hasattr(player, 'order'):
            for k in range(4):
                nx = x + CooDx[k]
                ny = y + CooDy[k]
                if self.isInBound(nx, ny):
                    if self.board[nx][ny] == self.color[player.order]:
                        return True
            return False
        else:
            for k in range(4):
                nx = x + CooDx[k]
                ny = y + CooDy[k]
                if self.isInBound(nx, ny):
                    if self.board[nx][ny] == self.color[player]:
                        return True
            return False

    def isCorner(self, player, x, y):
        if hasattr(player, 'order'):
            for k in range(4):
                nx = x + CooDp[k]
                ny = y + CooDq[k]
                if self.isInBound(nx, ny):
                    if self.board[nx][ny] == self.color[player.order]:
                        return True
            return False
        else:
            for k in range(4):
                nx = x + CooDp[k]
                ny = y + CooDq[k]
                if self.isInBound(nx, ny):
                    if self.board[nx][ny] == self.color[player]:
                        return True
            return False

    def getCorners(self, player):
        bg = (self.board == 0)

        cn = np.zeros((self.size, self.size), dtype = bool)
        cn[1:, 1:] |= (self.board[:-1, :-1] == self.color[player.order])
        cn[1:, :-1] |= (self.board[:-1, 1:] == self.color[player.order])
        cn[:-1, 1:] |= (self.board[1:, :-1] == self.color[player.order])
        cn[:-1, :-1] |= (self.board[1:, 1:] == self.color[player.order])

        ed = np.zeros((self.size, self.size), dtype = bool)
        ed[1:] |= (self.board[:-1] == self.color[player.order])
        ed[:-1] |= (self.board[1:] == self.color[player.order])
        ed[..., 1:] |= (self.board[..., :-1] == self.color[player.order])
        ed[..., :-1] |= (self.board[..., 1:] == self.color[player.order])
        
        ed = ~ed
        bg &= cn
        bg &= ed
        return np.where(bg == True)

    def canDrop(self, player, tile, x = -1, y = -1):
        
        '''
            !New: please use canDropList
            return True if player can drop the tile at (x, y).
            'tile' can be given in the form of pointlist or Tiles.
        '''

        if not isinstance(tile, list):
            raise TypeError
        coverCorner = False
        for (i, j) in tile:
            if not self.isInBound(i, j):
                raise Exception(u"超出边界")
            if self.board[i][j] != 0:
                raise Exception(u"和已有块重叠")
            if self.isAdj(player, i, j):
                raise Exception(u"边不能相邻")
            if self.isCorner(player, i, j) \
            or ((i, j) == (4, 4) and player == 0) \
            or ((i, j) == (9, 9) and player == 1):
                coverCorner = True
        if coverCorner:
            return True
        else:
            raise Exception(u"必须有角相邻")

    def dropTile(self, player, tile, x = -1, y = -1, varify = True):
        
        '''
            drop the tile at (x, y) and update the board.
            'tile' can be given in the form of pointlist or Tiles.
        '''

        if x == -1 and y == -1:
            if not isinstance(tile, list):
                raise TypeError
            if player < 0 or player >= self.playerNum:
                raise ValueError
            if not self.canDrop(player, tile, x, y):
                return False
            for (i, j) in tile:
                self.board[i][j] = self.color[player]
            return True
        else:
            if not isinstance(tile, Tiles):
                raise TypeError
            if tile.type == -1:
                raise ValueError
            if varify:
                if not self.canDrop(player, tile, x, y):
                    return False
            for (i, j) in tile.shape:
                self.board[x + i][y + j] = self.color[player.order]
            return True

    def retraceDrop(self, tile, x, y):
        for x0, y0 in tile.shape:
            self.board[x + x0][y + y0] = 0

    def print(self, fout = None):
        for i in range(self.size):
            for j in range(self.size):
                if fout is None:
                    print("%d " % self.board[i][j], end = '')
                else:
                    fout.write(chr(shape.colorAscii[self.board[i][j]]))
                    fout.write(chr(32))
            print() if fout is None else fout.write("\n")
    
    def clear(self):
        self.board = np.zeros((14, 14), dtype = int)

    def canDropPos(self, player, tile):

        '''
            the return format is same as numpy.where()
            return (xlist, ylist) where xlist and ylist are 
            1-d numpy.ndarray.
            if there is no legal position for tile, return a
            tuple contains an empty 1-d numpy.ndarray
        '''

        isEmpty = (self.board == self.color[player.order])
        if not (True in isEmpty):
            bg = np.zeros((self.size, self.size), dtype = bool)
            x0, y0 = [4, 4] if player.order == 0 else [9, 9]
            for (x, y) in tile.shape:
                bg[x0 - x, y0 - y] = True
            return np.where(bg == True)

        bg = np.ones((self.size, self.size), dtype = bool)
        ed = np.zeros((self.size, self.size), dtype = bool)
        cn = np.zeros((self.size, self.size), dtype = bool)
        mark = self.color[player.order]

        for (x, y) in tile.shape:
            bg[:self.size - x, :self.size - y] &= (self.board[x:, y:] == 0)
            if x != 0: 
                bg[self.size - x] = False
            if y != 0:
                bg[..., self.size - y] = False

            ed[:self.size - x - 1, :self.size - y] |= (self.board[x + 1:, y:] == mark)
            if x <= 1:
                ed[1 - x:, :self.size - y] |= (self.board[:self.size - 1 + x, y:] == mark)
            else:
                ed[:self.size - x + 1, :self.size - y] |= (self.board[x - 1:, y:] == mark)
            ed[:self.size - x, :self.size - y - 1] |= (self.board[x:, y + 1:] == mark)
            if y <= 1:
                ed[:self.size - x, 1 - y:] |= (self.board[x:, :self.size - 1 + y] == mark)
            else:
                ed[:self.size - x, :self.size - y + 1] |= (self.board[x:, y - 1:] == mark)

            cn[:self.size - x - 1, :self.size - y - 1] |= (self.board[x + 1:, y + 1:] == mark)
            if x <= 1 and y <= 1:
                cn[1 - x:, 1 - y:] |= (self.board[:self.size - 1 + x, :self.size - 1 + y] == mark)
                cn[1 - x:, :self.size - y - 1] |= (self.board[:self.size - 1 + x, y + 1:] == mark)
                cn[:self.size - x - 1, 1 - y:] |= (self.board[x + 1:, :self.size - 1 + y] == mark)
            elif x <= 1 and y > 1:
                cn[1 - x:, :self.size - y + 1] |= (self.board[:self.size - 1 + x, y - 1:] == mark)
                cn[1 - x:, :self.size - y - 1] |= (self.board[:self.size - 1 + x, y + 1:] == mark)
                cn[:self.size - x - 1, :self.size - y + 1] |= (self.board[x + 1:, y - 1:] == mark)
            elif x > 1 and y <= 1:
                cn[:self.size - x + 1, 1 - y:] |= (self.board[x - 1:, :self.size - 1 + y] == mark)
                cn[:self.size - x + 1, :self.size - y - 1] |= (self.board[x - 1:, y + 1:] == mark)
                cn[:self.size - x - 1, 1 - y:] |= (self.board[x + 1:, :self.size - 1 + y] == mark)
            elif x > 1 and y > 1:
                cn[:self.size - x + 1, :self.size - y - 1] |= (self.board[x - 1:, y + 1:] == mark)
                cn[:self.size - x - 1, :self.size - y + 1] |= (self.board[x + 1:, y - 1:] == mark)
                cn[:self.size - x + 1, :self.size - y + 1] |= (self.board[x - 1:, y - 1:] == mark)

        ed = ~ed 
        bg &= ed
        bg &= cn
        return np.where(bg == True)

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

        '''
            Get the board and player info from a matrix
        '''

        self.type = 0
        self.size = 14
        self.playerNum = 2
        self.color = [1, 2]
        self.board = np.asarray(matrix)
        visited = np.zeros((self.size, self.size), dtype = bool)

        def getTile(x, y, color, tilePoints):
            # floodfill
            visited[x][y] = True
            tilePoints.append([x, y])
            for k in range(4):
                nx = x + CooDx[k]
                ny = y + CooDy[k]
                if self.isInBound(nx, ny):
                    if matrix[nx][ny] == color and not visited[nx][ny]:
                        getTile(nx, ny, color, tilePoints)

        xlist, ylist = np.where(self.board != 0)

        for i in np.nditer(xlist):
            for j in np.nditer(ylist):
                if matrix[i][j] != 0 and not visited[i][j]:
                    tilePoints = []
                    minx = 14
                    miny = 14
                    getTile(i, j, matrix[i][j], tilePoints)
                    for x, y in tilePoints:
                        minx = min(minx, x)
                        miny = min(miny, y)
                    for k in range(len(tilePoints)):
                        tilePoints[k][0] = tilePoints[k][0] - minx
                        tilePoints[k][1] = tilePoints[k][1] - miny
                    tilePoints.sort()
                    tmpTile = []
                    for x, y in tilePoints:
                        tmpTile.append((x, y))
                    for t in range(21):
                        if shape.tileSizes[t] != len(tmpTile):
                            continue
                        if tmpTile in shape.shapeSet[t]:
                            player[matrix[i][j] - 1].used[t] = True
                            player[matrix[i][j] - 1].score += shape.tileSizes[t]
                            break

    def toMatrix(self):
        # return board as a 14*14 matrix
        return self.board

    def isOver(self, player):
        '''
            'player' here is a list of Player.
            If no player can drop a tile, return True.
        '''
        for pl in player:
            for t in range(21):
                if pl.used[t]:
                    continue
                for p in range(shape.tileMaxRotation[t]):
                    for q in [0, 1]:
                        tile = Tiles(t, p, q)
                        xlist = self.canDropPos(pl, tile)[0]
                        if xlist.size != 0:
                            return False
        return True

