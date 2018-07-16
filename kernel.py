
# core data
# search algorithm in this file

from board import Tiles, Board
import shape
import random

DecisionFunc = [] # the list of search functions
EvalFunc = [] # the list of evaluation functions

evalWeight = [20, 10]
# weights of greedyEval

minimaxDepth = 2
# depth = n means search n rounds 

'''
    All search functions have the same format
    of arguments and return values.

    Arguments:
        board: class Board. The current board.
        player: class Player. The current player.
        opponent: class Player. The opponent of the current player.
        **info: nothing

    Return values:
        list [
            the type of tile,
            rotation,
            flip, (rotation and flip infer the shape of tile)
            x,
            y (x and y represent the position of tile)
        ]
        If none of tile can be dropped, the functions return
            [-1, 0, 0, 0, 0]
'''

def randomGreedy(board, player, opponent, **info):

    '''
        Randomly choose one of the biggest tile 
        which can be dropped and drop it on a 
        random legal position.
    '''

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
    xlist = [i for i in range(board.size)]
    ylist = [i for i in range(board.size)]
    random.shuffle(xlist)
    random.shuffle(ylist)
    for size in range(5, 0, -1):
        if size > len(remain):
            continue
        random.shuffle(remain[size - 1])
        for i in range(len(remain[size - 1])):
            flag = False
            for x in xlist:
                for y in ylist:
                    direction = [i for i in range(8)]
                    random.shuffle(direction)
                    for k in direction:
                        tile = Tiles(remain[size - 1][i], k % 4, k // 4)
                        flag = board.canDrop(player, tile, x, y)
                        if flag:
                            return [
                                 remain[size - 1][i], # type of tile
                                 k % 4, # rotation
                                 k // 4, # flip
                                 x, # x
                                 y # y
                            ]
    return [-1, 0, 0, 0, 0]

DecisionFunc.append(randomGreedy)

def greedyEval(board, player, opponent):

    '''
        Evaluation function.
        score = player.score * w1 
              + the difference of valid corners
                between the player and opponents * w2
    '''

    def validCornerNumber(player):
        return len(board.getCorners(player))

    score = (player.score - opponent.score) * evalWeight[0]
    cor = validCornerNumber(player) - validCornerNumber(opponent)
    score += cor * evalWeight[1]
    score += random.random() 
    # avoid the same choice 
    return score

EvalFunc.append(greedyEval)

def greedy(board, player, opponent, evalFunc = 0, **info):

    '''
        Enumerate all possible drops, and get a score
        using EvalFunc[evalFunc]
    '''

    if 'setEvalFunc' in info:
        evalFunc = info['setEvalFunc']

    global evalWeight
    if 'setEvalWeight' in info:
        evalWeight = info['setEvalWeight']

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
                        result = board.dropTile(player, tile, x, y)
                        if result:
                            player.score += tile.size
                            ss = set()
                            for coo in shape.cornerSet[tile.type][tile.rotation + tile.flip * 4]:
                                if board.isInBound(x + coo[0], y + coo[1]):
                                    ss.update([(x + coo[0], y + coo[1])])
                            player.tmpSet.append(ss)
                            score = EvalFunc[evalFunc](board, player, opponent)
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
                            player.tmpSet.pop()
                            player.score -= tile.size
    if maxScore > -32768:
        return maxDecision
    else:
        return [-1, 0, 0, 0, 0]

DecisionFunc.append(greedy)

def _alphaBeta(depth, board, player, opponent, evalFunc, alpha, beta, desPlayer):

    '''
        Internal recursive alphabeta pruning
    '''

    if depth == minimaxDepth:
        return EvalFunc[evalFunc](board, player, opponent)
    bestMove = [-1, 0, 0, 0, 0]
    for i in range(20, -1, -1):
        if player.used[i]:
            continue
        for x in range(board.size):
            for y in range(board.size):
                for p in range(shape.tileMaxRotation[i]):
                    for q in range(2):
                        tile = Tiles(i, p, q)
                        result = board.dropTile(player, tile, x, y)
                        if result:
                            player.score += tile.size
                            ss = set()
                            for coo in shape.cornerSet[tile.type][tile.rotation + tile.flip * 4]:
                                if board.isInBound(x + coo[0], y + coo[1]):
                                    ss.update([(x + coo[0], y + coo[1])])
                            player.tmpSet.append(ss)
                            score = -_alphaBeta(depth + 1, board, opponent, player, evalFunc, -beta, -alpha, desPlayer)
                            board.retraceDrop(tile, x, y)
                            player.tmpSet.pop()
                            player.score -= tile.size
                            if score >= alpha:
                                alpha = score
                                if depth == 0:
                                    bestMove = [i, p, q, x, y]
                                    if alpha >= beta:
                                        return [alpha, bestMove]
                                else:
                                    if alpha >= beta:
                                        return alpha
    return alpha if depth != 0 else [alpha, bestMove]

def alphaBeta(board, player, opponent, evalFunc = 0, **info):

    '''
        Alphabeta pruning
    '''

    global evalWeight
    if 'setEvalFunc' in info:
        evalFunc = info['setEvalFunc']
    if 'setEvalWeight' in info:
        evalWeight = info['setEvalWeight']
        
    alpha = -32768
    beta = 32767
    bestMove = _alphaBeta(0, board, player, opponent, evalFunc, alpha, beta, player.order)
    return bestMove[1]

DecisionFunc.append(alphaBeta)
