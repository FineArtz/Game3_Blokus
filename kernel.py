
# core data
# search algorithm in this file

from board import Tiles, Board
import shape
import random
import copy
import numpy as np 

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

def greedyEval(board, player, opponent, **info):

    '''
        Evaluation function.
        score = player.score * w1 
              + the difference of valid corners
                between the player and opponents * w2
    '''

    def validCornerNumber(player):
        return board.getCorners(player)[0].size

    score = (player.score - opponent.score) * evalWeight[0]
    cor = validCornerNumber(player) - validCornerNumber(opponent)
    score += cor * evalWeight[1]
    score += random.random() 
    # avoid the same choice 
    return score

EvalFunc.append(greedyEval)

def mctsEval(board, player, opponent, **info):
    score = 0
    rev = False
    tot = 6
    stp = 4
    if 'setTot' in info:
        tot = info['setTot']
    if 'setReverse' in info:
        rev = info['setReverse']
    if 'setStep' in info:
        stp = info['setStep']

    tmpDecMaker = [player.decisionMaker, opponent.decisionMaker]
    player.decisionMaker = opponent.decisionMaker = randomRandom
    tmpPlayer = player
    tmpOpponent = opponent
    if rev:
        tmpPlayer = opponent
        tmpOpponent = player
    initScore = greedyEval(board, tmpPlayer, tmpOpponent)

    for game in range(tot):
        tmpHistory = []
        flag = False
        for step in range(stp):
            flag = False
            result = tmpPlayer.action(board, tmpOpponent, setEvalFunc = 0)
            if result['action']:
                flag = True
                result['id'] = 0
                tmpHistory.append(result)
            result = tmpOpponent.action(board, tmpPlayer, setEvalFunc = 0)
            if result['action']:
                flag = True
                result['id'] = 1
                tmpHistory.append(result)
            if not flag:
                break
        if flag:
            if greedyEval(board, tmpPlayer, tmpOpponent) > initScore:
                score += 1
        else:
            if tmpPlayer.score > tmpOpponent.score:
                score += 1
        for h in tmpHistory:
            if h['id'] == 0:
                tmpPlayer.used[h['tileType']] = False
                tmpPlayer.score -= shape.tileSizes[h['tileType']]
            else:
                tmpOpponent.used[h['tileType']] = False
                tmpOpponent.score -= shape.tileSizes[h['tileType']]
            board.retraceDrop(Tiles(h['tileType'], h['rotation'], h['flip']), h['x'], h['y'])

    player.decisionMaker, opponent.decisionMaker = tmpDecMaker
    return score / tot if not rev else 1 - score / tot

EvalFunc.append(mctsEval)

def randomRandom(board, player, opponent, **info):

    '''
        Purely random
    '''

    tileList = np.where(player.used == False)[0]
    used = np.zeros(21, dtype = bool)
    cnt = 0

    while cnt < tileList.size:
        t = np.random.choice(tileList)
        while used[t]:
            t = np.random.choice(tileList)
        direction = np.random.permutation(shape.tileMaxRotation[t])
        for d in direction:
            f = 0
            tile = Tiles(t, d, f)
            possiblePos = board.canDropPos(player, tile)
            if possiblePos[0].size != 0:
                i = np.random.choice(possiblePos[0].size)
                x, y = possiblePos[0][i], possiblePos[1][i]
                return [t, d, f, x, y]
            f = 1
            tile = Tiles(t, d, f)
            possiblePos = board.canDropPos(player, tile)
            if possiblePos[0].size != 0:
                i = np.random.choice(possiblePos[0].size)
                x, y = possiblePos[0][i], possiblePos[1][i]
                return [t, d, f, x, y]
        used[t] = True
        cnt += 1
    return [-1, 0, 0, 0, 0]

DecisionFunc.append(randomRandom)

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
    for size in range(5, 0, -1):
        if size > len(remain):
            continue
        random.shuffle(remain[size - 1])
        for i in range(len(remain[size - 1])):
            direction = [i for i in range(8)]
            random.shuffle(direction)
            for k in direction:
                tile = Tiles(remain[size - 1][i], k % 4, k // 4)
                xlist, ylist = board.canDropPos(player, tile)
                if xlist.size == 0:
                    continue
                j = np.random.choice(xlist.size)
                return [
                        remain[size - 1][i], # type of tile
                        k % 4, # rotation
                        k // 4, # flip
                        xlist[j], # x
                        ylist[j] # y
                ]
    return [-1, 0, 0, 0, 0]

DecisionFunc.append(randomGreedy)

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
    remain = np.where(player.used == False)[0]
    if remain.size == 0:
        return [-1, 0, 0, 0, 0]
    remain = remain[::-1]
    for i in remain:
        for p in range(shape.tileMaxRotation[i]):
            for q in [0, 1]:
                tile = Tiles(i, p, q)
                xlist, ylist = board.canDropPos(player, tile)
                if xlist.size == 0:
                    continue
                for k in range(xlist.size):
                    x = xlist[k]
                    y = ylist[k]
                    result = board.dropTile(player, tile, x, y, False)
                    if result:
                        player.score += tile.size
                        player.used[tile.type] = True
                        score = EvalFunc[evalFunc](board, player, opponent, setReverse = True)
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
                        player.used[tile.type] = False
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
    remain = np.where(player.used == False)[0]
    remain = remain[::-1] 
    #reverse the array to search in a specific order

    for i in remain:
        for p in range(shape.tileMaxRotation[i]):
            for q in [0, 1]:
                tile = Tiles(i, p, q)
                xlist, ylist = board.canDropPos(player, tile)
                if xlist.size == 0:
                    continue
                for k in range(xlist.size):
                    x = xlist[k]
                    y = ylist[k]
                    result = board.dropTile(player, tile, x, y, False)
                    if result:
                        player.score += tile.size

                        score = -_alphaBeta(depth + 1, board, opponent, player, evalFunc, -beta, -alpha, desPlayer)

                        board.retraceDrop(tile, x, y)
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

    if 'setEvalFunc' in info:
        evalFunc = info['setEvalFunc']

    global evalWeight
    if 'setEvalWeight' in info:
        evalWeight = info['setEvalWeight']
        
    alpha = -32768
    beta = 32767
    bestMove = _alphaBeta(0, board, player, opponent, evalFunc, alpha, beta, player.order)
    return bestMove[1]

DecisionFunc.append(alphaBeta)

def mcts(board, player, opponent, evalFunc = 0, **info):

    '''
        Enumerate all possible drops and select the best
        5 of them, then use mcstEval to reevaluate them
    '''

    if 'setEvalFunc' in info:
        evalFunc = info['setEvalFunc']

    global evalWeight
    if 'setEvalWeight' in info:
        evalWeight = info['setEvalWeight']
        
    totGame = 20
    if 'setTotalGame' in info:
        totGame = info['setTotalGame']

    maxDecision = []
    remain = np.where(player.used == False)[0]

    for i in remain:
        for p in range(shape.tileMaxRotation[i]):
            for q in [0, 1]:
                tile = Tiles(i, p, q)
                xlist, ylist = board.canDropPos(player, tile)
                if xlist.size == 0:
                    continue
                for k in range(xlist.size):
                    x = xlist[k]
                    y = ylist[k]
                    board.dropTile(player, tile, x, y, False)
                    player.score += tile.size
                    player.used[tile.type] = True
                    score = EvalFunc[evalFunc](board, player, opponent, setReverse = True)
                    if len(maxDecision) < 5:
                        maxDecision.append({
                            'score' : score,
                            'tileType' : i, # type of tile
                            'rot' : p, # rotation
                            'flip' : q, # flip
                            'x' : x, # x
                            'y' : y # y
                        })
                    elif score > maxDecision[-1]['score']:
                        m = 4
                        while m > 0:
                            if maxDecision[m]['score'] > score:
                                break
                            maxDecision[m] = maxDecision[m - 1]
                            m -= 1
                        maxDecision[m] = {
                            'score' : score,
                            'tileType' : i, # type of tile
                            'rot' : p, # rotation
                            'flip' : q, # flip
                            'x' : x, # x
                            'y' : y # y
                        }
                    board.retraceDrop(tile, x, y)
                    player.used[tile.type] = False
                    player.score -= tile.size
    if maxDecision != []:
        maxscore = -1
        maxd = -1
        for i, dec in enumerate(maxDecision):
            tile = Tiles(dec['tileType'], dec['rot'], dec['flip'])
            board.dropTile(player, tile, dec['x'], dec['y'], False)
            player.used[dec['tileType']] = True
            score = mctsEval(board, player, opponent, setTot = totGame, setReverse = True)
            if score > maxscore:
                maxd = i
            board.retraceDrop(tile, dec['x'], dec['y'])
            player.used[dec['tileType']] = False
        return [
            maxDecision[maxd]['tileType'],
            maxDecision[maxd]['rot'],
            maxDecision[maxd]['flip'],
            maxDecision[maxd]['x'],
            maxDecision[maxd]['y']
        ]
    else:
        return [-1, 0, 0, 0, 0]

DecisionFunc.append(mcts)
