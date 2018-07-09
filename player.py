
# Definition of players
# interact with board

from kernel import DecisionFunc
from board import Tiles, Board

class Player(object):
    def __init__(self, type = -1, order = 0, level = 0):
        if type == -1:
            pass
        else:
            self.type = type
            self.order = order
            if type is 0:
                self.tiles = [Tiles(i) for i in range(21)]
                self.used = [False for i in range(21)]
                self.score = 0
                self.decisionMaker = DecisionFunc[level]

    def action(self, board, opponent):
        if not isinstance(board, Board):
            raise TypeError
        if self.type != board.type or self.order >= board.playerNum:
            raise ValueError
        tileType, rot, flp, x, y = self.decisionMaker(board, self, opponent)
        if tileType != -1:
            tile = Tiles(tileType, rot, flp)
            board.dropTile(self.order, tile, x, y)
            self.used[tileType] = True
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

