
# Definition of players
# interact with board

from kernel import DecisionFunc
from board import Tiles, Board, CooDp, CooDq
from shape import cornerSet
import sys, argparse
import json

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
                self.tmpSet = []
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
            if board.board[i][j] == 0:
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
            board.dropTile(self, tile, x, y)
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

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help = "AI config")
    parser.add_argument("--input", help = "input history")
    args = parser.parse_args()

    """
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
    """

    board = Board()
    output = {}
    matrix = []
    player = None
    opponent = None

    jsInfo = args.input
    info = json.loads(jsInfo)
    if info['history'] != []:
        playerOrder = info['history'][-1]['action_player_id']
        if playerOrder == -1:
            playerOrder = 0
        else:
            playerOrder ^= 1
        player = Player(0, playerOrder, 0)
        opponent = Player(0, playerOrder ^ 1, 0)
        matrix = info['history'][-1]['state']
    else:
        matrix = [[0 for i in range(14)] for j in range(14)]
        player = Player(0, 0, 0)
        opponent = Player(0, 1, 0)
        
    board.parseFromMatrix(matrix, [player, opponent])
    result = player.action(board, opponent)

    if result['action']:
        output['status'] = "Success"
        output['is_pass'] = False
        output['action'] = []
        tile = Tiles(result['tileType'], result['rotation'], result['flip'])
        x = result['x']
        y = result['y']
        for (i, j) in tile.shape:
            output['action'].append({
                "row" : x + i,
                "col" : y + j
            })
        print(json.dumps(output))
    else:
        output['status'] = "Success"
        output['is_pass'] = True
        output['action'] = []
        print(json.dumps(output))

