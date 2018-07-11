
# Definition of players
# interact with board

from kernel import DecisionFunc
from board import Tiles, Board, CooDp, CooDq
from shape import cornerSet
import sys

class Player(object):

    '''
        type: the type of game. Blokus Duo is type 0. 
        order: the order of player, 0 or 1
        level: the level of AI player. 
            level = -1 represents human player
        info: other info

        Invoke 'action' to drop a tile.
    '''

    def __init__(self, type = -1, order = 0, level = 0, **info):
        if type == -1:
            pass
        else:
            self.type = type
            self.order = order
            if type is 0:
                self.tiles = [Tiles(i) for i in range(21)]
                self.used = [False for i in range(21)]
                self.score = 0
                if order == 0:
                    self.corners = set([(4, 4)])
                else:
                    self.corners = set([(9, 9)])
                if level == -1:
                    self.decisionMaker = None
                else:
                    self.decisionMaker = DecisionFunc[level]
                self.w1, self.w2 = [20, 10]
                if 'setWeight' in info:
                    self.w1, self.w2 = info['setWeight']

    def updateCorners(self, board):
        tmpSet = set()
        for (i, j) in self.corners:
            if board.board[i][j] == self.order + 1:
                tmpSet.update([(i, j)])
            elif board.board[i][j] == 0:
                if board.isCorner(self.order, i, j):
                    tmpSet.update([(i, j)])
        self.corners = tmpSet

    def action(self, board, opponent):
        if self.decisionMaker is None:
            raise ValueError("The player is human")
        if not isinstance(board, Board):
            raise TypeError
        if self.type != board.type or self.order >= board.playerNum:
            raise ValueError
        tileType, rot, flp, x, y = self.decisionMaker(board, self, opponent, setEvalWeight = [self.w1, self.w2])
        if tileType != -1:
            tile = Tiles(tileType, rot, flp)
            board.dropTile(self.order, tile, x, y)
            self.used[tileType] = True
            for coo in cornerSet[tileType][rot + flp * 4]:
                if board.isInBound(x + coo[0], y + coo[1]):
                    self.corners.update([(x + coo[0], y + coo[1])])
            self.score = self.score + self.tiles[tileType].size
            return {
                "action" : True,
                "tileType" : tileType,
                "rotation" : rot,
                "flip" : flp,
                "x" : x,
                "y" : y
            }
        else:
            return {
                "action" : False
            }

if __name__ == '__main__':
    argc = len(sys.argv)
    
    '''
        -l level: set the level of AI player as 'level'
        default: -l 0
    '''
    lv = 0
    if '-l' in sys.argv[1:]:
        argpos = sys.argv.index('-l')
        lv = int(sys.argv[argpos + 1])
    
    '''
        -w w1 w2: weights for evaluation functions
        default: -w 20 10
    '''
    w1 = 20
    w2 = 10
    if '-w' in sys.argv[1:]:
        argpos = sys.argv.index('-w')
        w1 = int(sys.argv[argpos + 1])
        w2 = int(sys.argv[argpos + 2])

    board = Board()

    playerOrder = int(input())
    player = Player(0, playerOrder, lv, setEvalWeight = [w1, w2])
    opponent = Player(0, playerOrder ^ 1, 0)

    tileSize = int(input())
    for i in range(tileSize):
        x, y = list(map(int, input().split(' ')))
    
    matrix = []
    for i in range(14):
        matrix.append(list(map(int, input().split(' '))))
    
    board.parseFromMatrix(matrix, [player, opponent])

    result = player.action(board, opponent)
    if result['action']:
        tile = Tiles(result['tileType'], result['rotation'], result['flip'])
        print("%d %d" % (playerOrder, tile.size))
        for coo in tile.shape:
            print("%d %d" % (result['x'] + coo[0], result['y'] + coo[1]))
    else:
        print("%d -1" % playerOrder)

