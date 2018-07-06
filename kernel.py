
# core data
# search algorithm in this file

from board import Tiles, Board
import shape
import random

DecisionFunc = []
EvalFunc = []

def randomGreedy(board, order, used, **info):
    remain = []
    nowSize = 0
    for i in range(21):
        if not used[i]:
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
                        tile = Tiles(remain[size - 1][i], k // 4, k % 4)
                        flag = board.dropTile(order, tile, x, y)
                        if flag:
                            return [
                                 remain[size - 1][i], # type of tile
                                 k // 4, # rotation
                                 k % 4, # flip
                                 x, # x
                                 y # y
                            ]
            del remain[size - 1][i]
            num = num - 1
    return [-1, 0, 0, 0, 0]

DecisionFunc.append(randomGreedy)

def greedyEval(board, order, w1 = 10, w2 = 10):
    def validCornerNumber(order):
        tmpSet = board.cornerSets[order] | board.tmpSets[order]
        Len = 0
        for p in tmpSet:
            if not board.isAdj(order, p[0], p[1]):
                Len = Len + 1
        return Len

    score = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.board[i][j] == board.color[order] or board.board[i][j] == board.tmpColor[order]:
                score = score + 1
    score = score * w1
    cor = 0
    for i in range(board.playerNum):
        cor = cor + (1 if i == order else -1) * validCornerNumber(i)
    score = score + cor * w2
    score = score + random.random()
    return score

EvalFunc.append(greedyEval)

def greedy(board, order, used, evalFunc = 0, **info):
    maxScore = -32768
    maxDecision = []
    for i in range(20, -1, -1):
        if used[i]:
            continue
        for x in range(board.size):
            for y in range(board.size):
                for k in range(8):
                    tile = Tiles(i, k // 4, k % 4)
                    result = board.tryDrop(order, tile, x, y)
                    if result != False:
                        score = EvalFunc[evalFunc](board, order)
                        if score > maxScore:
                            maxScore = score
                            maxDecision = [
                                i, # type of tile
                                k // 4, # rotation
                                k % 4, # flip
                                x, # x
                                y # y
                            ]
                        board.retraceDrop(order)
    if maxScore > -32768:
        return maxDecision
    else:
        return [-1, 0, 0, 0, 0]

DecisionFunc.append(greedy)
