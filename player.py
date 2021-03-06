
# Definition of players
# interact with board

from kernel import DecisionFunc
from board import Tiles, Board
from shape import cornerSet, tileSizes
import sys, argparse
import json
import numpy as np 

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
                self.used = np.zeros(21, dtype = bool)
                self.score = 0
                if level == -1:
                    self.decisionMaker = None
                else:
                    self.decisionMaker = DecisionFunc[level]
                self.w1, self.w2 = [20, 10]
                if 'setWeight' in info:
                    self.w1, self.w2 = info['setWeight']

    def clear(self):
        self.used = np.zeros(21, dtype = bool)
        self.score = 0

    def action(self, board, opponent, **info):
        if self.decisionMaker is None:
            raise ValueError("The player is human")
        if not isinstance(board, Board):
            raise TypeError
        if self.type != board.type or self.order >= board.playerNum:
            raise ValueError
        if 'setEvalWeight' in info:
            self.w1, self.w2 = info['setEvalWeight']
        ef = 0
        if 'setEvalFunc' in info:
            ef = info['setEvalFunc']
        tileType, rot, flp, x, y = self.decisionMaker(board, self, opponent, \
                                    setEvalWeight = [self.w1, self.w2], setEvalFunc = ef)
        if tileType != -1:
            tile = Tiles(tileType, rot, flp)
            board.dropTile(self, tile, x, y, False)
            self.used[tileType] = True
            self.score = self.score + tileSizes[tileType]
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
    parser.add_argument("--input", required = True, help = "input history")
    parser.add_argument("--config", required = True, help = "AI config")
    args = parser.parse_args()

    board = Board()
    output = {}
    matrix = []
    player = None
    opponent = None

    conf = json.loads(args.config)
    evalWeight = conf.get('eval_weight', [10, 20])
    evalFunc = conf.get('eval_func', 0)
    lv = conf.get('AI_level', 0)

    info = json.loads(args.input)
    if info['history'] != []:
        playerOrder = info['history'][-1]['action_player_id']
        if playerOrder == -1:
            playerOrder = 0
        else:
            playerOrder ^= 1
        player = Player(0, playerOrder, lv)
        opponent = Player(0, playerOrder ^ 1, 0)
        matrix = info['history'][-1]['state']
    else:
        matrix = [[0 for i in range(14)] for j in range(14)]
        player = Player(0, 0, lv)
        opponent = Player(0, 1, 0)

    if playerOrder == 0:
        board.parseFromMatrix(matrix, [player, opponent])
    else:
        board.parseFromMatrix(matrix, [opponent, player])
    
    result = player.action(board, opponent, setEvalWeight = evalWeight, setEvalFunc = evalFunc)

    if result['action']:
        output['status'] = "Success"
        output['is_pass'] = False
        output['action'] = []
        tile = Tiles(result['tileType'], result['rotation'], result['flip'])
        x = result['x']
        y = result['y']
        for (i, j) in tile.shape:
            output['action'].append({
                "row" : int(x + i),
                "col" : int(y + j)
            })
        print(json.dumps(output))
    else:
        output['status'] = "Success"
        output['is_pass'] = True
        output['action'] = []
        print(json.dumps(output))

