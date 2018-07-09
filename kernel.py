
# core data
# search algorithm in this file

from board import Tiles, Board
import shape
import random

DecisionFunc = []
EvalFunc = []

minimaxDepth = 2
# depth = n means search n rounds 

def randomGreedy(board, player, opponent, **info):
    remain = []
    nowSize = 0
    for i in range(21):
        if not player.used[i]:
            if nowSize == shape.tileSizes[i]:
                remain[nowSize - 1].append(i)
            else:
                remain.append([])
                nowSize = nowSize + 1
                remain[nowSize - 1].append(i)
    for size in range(5, 0, -1):
        if size > len(remain):
            continue
        while not remain[size - 1] == []:
            num = len(remain[size - 1])
            i = random.randrange(0, num)
            flag = False
            for x in range(board.size):
                for y in range(board.size):
                    direction = []
                    dsize = 0
                    while dsize < 8:
                        d = random.randrange(8)
                        if not d in direction:
                            direction.append(d)
                            dsize = dsize + 1
                    for k in direction:
                        tile = Tiles(remain[size - 1][i], k % 4, k // 4)
                        flag = board.canDrop(player.order, tile, x, y)
                        if flag:
                            return [
                                 remain[size - 1][i], # type of tile
                                 k % 4, # rotation
                                 k // 4, # flip
                                 x, # x
                                 y # y
                            ]
            del remain[size - 1][i]
            num = num - 1
    return [-1, 0, 0, 0, 0]

DecisionFunc.append(randomGreedy)

def greedyEval(board, player, w1 = 10, w2 = 10):
    def validCornerNumber(order):
        return len(board.getCorners(order))

    score = player.score * w1
    cor = 0
    for i in range(board.playerNum):
        cor = cor + (1 if i == player.order else -1) * validCornerNumber(i)
    score = score + cor * w2
    score = score + random.random()
    return score

EvalFunc.append(greedyEval)

def greedy(board, player, opponent, evalFunc = 0, **info):
    maxScore = -32768
    maxDecision = []
    for i in range(20, -1, -1):
        if player.used[i]:
            continue
        for x in range(board.size):
            for y in range(board.size):
                for p in range(shape.tileMaxRotation[i]):
                    for q in range(2):
                        tile = Tiles(i, p, q)
                        result = board.dropTile(player.order, tile, x, y)
                        if result:
                            player.score = player.score + tile.size
                            score = EvalFunc[evalFunc](board, player)
                            if score > maxScore:
                                maxScore = score
                                maxDecision = [
                                    i, # type of tile
                                    p, # rotation
                                    q, # flip
                                    x, # x
                                    y # y
                                ]
                            board.retraceDrop(tile, x, y)
                            player.score = player.score - tile.size
    if maxScore > -32768:
        return maxDecision
    else:
        return [-1, 0, 0, 0, 0]

DecisionFunc.append(greedy)

def _alphaBeta(depth, board, player, opponent, evalFunc, alpha, beta, desPlayer):
    if depth == minimaxDepth:
        return EvalFunc[evalFunc](board, player)
    if player.order != desPlayer:
        for i in range(20, -1, -1):
            if player.used[i]:
                continue
            for x in range(board.size):
                for y in range(board.size):
                    for p in range(shape.tileMaxRotation[i]):
                        for q in range(2):
                            tile = Tiles(i, p, q)
                            result = board.dropTile(player.order, tile, x, y)
                            if result:
                                player.score = player.score + tile.size
                                score = _alphaBeta(depth + 1, board, opponent, player, evalFunc, alpha, beta, desPlayer)
                                board.retraceDrop(tile, x, y)
                                player.score = player.score - tile.size
                                if score < beta:
                                    beta = score
                                    if alpha >= beta:
                                        return alpha 
        return beta
    else:
        bestMove = [-1, 0, 0, 0, 0]
        for i in range(20, -1, -1):
            if player.used[i]:
                continue
            for x in range(board.size):
                for y in range(board.size):
                    for p in range(shape.tileMaxRotation[i]):
                        for q in range(2):
                            tile = Tiles(i, p, q)
                            result = board.dropTile(player.order, tile, x, y)
                            if result:
                                player.score = player.score + tile.size
                                score = _alphaBeta(depth + 1, board, opponent, player, evalFunc, alpha, beta, desPlayer)
                                board.retraceDrop(tile, x, y)
                                player.score = player.score - tile.size
                                if score > alpha:
                                    alpha = score
                                    if depth == 0:
                                        bestMove = [i, p, q, x, y]
                                        if alpha >= beta:
                                            return bestMove
                                    else:
                                        if alpha >= beta:
                                            return beta
        return alpha if depth != 0 else bestMove

def alphaBeta(board, player, opponent, evalFunc = 0, **info):
    global minimaxDepth
    if 'setMaxDepth' in info:
        minimaxDepth = info['setMaxDepth']
    bestMove = _alphaBeta(0, board, player, opponent, evalFunc, -32768, 32767, player.order)
    return bestMove

DecisionFunc.append(alphaBeta)
