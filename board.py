
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
        tmp = copy.copy(player.corners)
        for s in player.tmpSet:
            tmp = tmp | s
        ret = set()
        for (i, j) in tmp:
            if self.board[i][j] == 0 and not self.isAdj(player, i, j):
                ret.update([(i, j)])
        return ret

    def canDrop(self, player, tile, x = -1, y = -1):
        '''
            return True if player can drop the tile at (x, y).
            'tile' can be given in the form of pointlist or Tiles.
        '''
        if x == -1 and y == -1:
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
        else:
            if not isinstance(tile, Tiles):
                raise TypeError
            if tile.type == -1:
                raise ValueError
            coverCorner = False
            for (i, j) in tile.shape:
                if not self.isInBound(x + i, y + j):
                    return False
                if self.board[x + i][y + j] != 0:
                    return False
                if self.isAdj(player, x + i, y + j):
                    return False
                if (x + i, y + j) in player.corners \
                or ((x + i, y + j) == (4, 4) and player.order == 0) \
                or ((x + i, y + j) == (9, 9) and player.order == 1):
                    coverCorner = True
            return coverCorner

    def dropTile(self, player, tile, x = -1, y = -1):
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
            if not self.canDrop(player, tile, x, y):
                return False
            for (i, j) in tile.shape:
                self.board[x + i][y + j] = self.color[player.order]
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

        '''
            Get the board and player info from a matrix
        '''

        self.type = 0
        self.size = 14
        self.playerNum = 2
        self.color = [1, 2]
        self.board = copy.deepcopy(matrix)
        visited = [[False for i in range(14)] for j in range(14)]

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

        for i in range(14):
            for j in range(14):
                if matrix[i][j] != 0 and not visited[i][j]:
                    tilePoints = []
                    minx = 14
                    miny = 14
                    getTile(i, j, matrix[i][j], tilePoints)
                    for [x, y] in tilePoints:
                        minx = min(minx, x)
                        miny = min(miny, y)
                    for k in range(len(tilePoints)):
                        tilePoints[k][0] = tilePoints[k][0] - minx
                        tilePoints[k][1] = tilePoints[k][1] - miny
                    tilePoints.sort()
                    tmpTile = []
                    for [x, y] in tilePoints:
                        tmpTile.append((x, y))
                    for t in range(21):
                        if shape.tileSizes[t] != len(tmpTile):
                            continue
                        if tmpTile in shape.shapeSet[t]:
                            u = shape.shapeSet[t].index(tmpTile)
                            player[matrix[i][j] - 1].used[t] = True
                            player[matrix[i][j] - 1].score += shape.tileSizes[t]
                            for (x, y) in shape.cornerSet[t][u]:
                                nx = minx + x
                                ny = miny + y
                                if nx >= 0 and nx < 14 and ny >= 0 and ny < 14:
                                    player[matrix[i][j] - 1].corners.update([(nx, ny)])
                            break
        player[0].updateCorners(self)
        player[1].updateCorners(self)

    def toMatrix(self):
        # return board as a 14*14 matrix
        return self.board

    def isOver(self, player):
        '''
            'player' here is a list of Player.
            If no player can drop a tile, return True.
        '''
        for i in range(self.playerNum):
            for t in range(21):
                if player[i].used[t]:
                    continue
                for x in range(self.size):
                    for y in range(self.size):
                        for p in range(shape.tileMaxRotation[i]):
                            for q in range(2):
                                tile = Tiles(i, p, q)
                                if self.canDrop(player[i], tile, x, y):
                                    return False
        return True

