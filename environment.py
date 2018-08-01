
# environment

import sys, os
import argparse
import json
from board import Tiles, Board
from player import Player
import shape

def pprint(thing):
    sys.stdout.write(thing + '\n')
    sys.stdout.flush()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    player = []

    parser.add_argument("--players_allocate", default = "AI,AI", help = "indicate player type and order")
    parser.add_argument("--extra", help = "extra info")
    args = parser.parse_args()

    if args.players_allocate:
        pa = args.players_allocate.split(',')
        if len(pa) != 2:
            raise ValueError("--player_allocate must have two arguments!")
        player.append(Player(0, 0, -1))
        player.append(Player(0, 1, -1))

    if not args.extra is None:
        pass

    board = Board()
    history = {}
    history['step'] = []

    output = {}
    output["status"] = "Success"
    output["action_player_id"] = 0
    output["state"] = board.board

    pprint(json.dumps(output))
    isOver = False

    while True:
        jsInfo = sys.stdin.readline().rstrip()
        info = json.loads(jsInfo)
        act = info['action']
        isPass = info['is_pass']
        playerOrder = info['action_player_id']

        output = {}
        if isPass:
            if isOver:
                output['status'] = "Over"
                output['result'] = {
                    "record" : json.dumps(history),
                    "score" : [p.score for p in player],
                    "winner_id" : 0 
                }
                if player[0].score < player[1].score:
                    output['result']['winner_id'] = 1
                elif player[0].score == player[1].score:
                    output['result']['winner_id'] = -1
                pprint(json.dumps(output))
                break
            output["status"] = "Success"
            output["action_player_id"] = playerOrder ^ 1
            output["state"] = board.board
            pprint(json.dumps(output))
            isOver = True
            continue

        isOver = False
        tile = []
        tileSize = len(act)
        minx = 14
        miny = 14
        for i in range(tileSize):
            x = act[i]['row']
            y = act[i]['col']
            tile.append([x, y])
            minx = min(minx, x)
            miny = min(miny, y)
        try:
            result = board.dropTile(playerOrder, tile)
        except Exception as e:
            output['status'] = "Error"
            output['reason'] = str(e)
            pprint(json.dumps(output))
            break
        else:
            if result:
                output = {}
                step = {}
                step["player"] = playerOrder
                step["action"] = act
                step["state"] = {}
                history["step"].append(step)

                for i in range(tileSize):
                    tile[i][0] -= minx
                    tile[i][1] -= miny
                tile.sort()
                rotf = 0
                for t in range(21):
                    if shape.tileSizes[t] != tileSize:
                        continue
                    if tile in shape.shapeSet[t]:
                        player[playerOrder].used[t] = True
                        rotf = shape.shapeSet[t].index[tile]
                        break
                player[playerOrder].score += tileSize
                for (i, j) in shape.cornerSet[t][rotf]:
                    if board.isInBound(minx + i, miny + j):
                        if board.board[minx + i][miny + j] == 0:
                            player[playerOrder].corners.update([(minx + i, miny + j)])
                
                output['status'] = "Success"
                output['action_player_id'] = playerOrder ^ 1
                output['state'] = board.board
                pprint(json.dumps(output))

