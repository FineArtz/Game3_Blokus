
# analyse board and get winning rate

from kernel import analBoard
from board import Tiles, Board
from shape import shapeSet
from player import Player
import sys, argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required = True, help = "board state")
    parser.add_argument("--player_id", required = True, type = True, help = 'player id')
    args = parser.parse_args()

    board = Board()

    p_id = args.player_id
    player = Player(0, p_id, 0)
    opponent = Player(0, p_id ^ 1, 0)

    matrix = json.loads(args.state)
    if p_id == 0:
        board.parseFromMatrix(matrix, [player, opponent])
    else:
        board.parseFromMatrix(matrix, [opponent, player])

    result = analBoard(board, player, opponent)
    def wr(pack):
        return pack['winningRate']
    result.sort(key = wr, reverse = True)

    output = []
    for r in result:
        tile = Tiles(r['tileType'], r['rotation'], r['flip'])
        x = r['x']
        y = r['y']
        action = []
        for i, j in tile.shape:
            action.append({
                "row" : x + i,
                "col" : y + j
            }) 
        output.append({
            "action" : action,
            "winning_rate" : r['winningRate']
        })
    print(json.dumps(output))
    