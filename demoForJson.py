
# game engine

from board import Tiles, Board
from player import Player
import shape
import sys

if __name__ == '__main__':

    argc = len(sys.argv)

    board = Board()
    player = []
    if '-p' in sys.argv[1:]:
        argpos = sys.argv.index('-p')
        pType1 = int(sys.argv[argpos + 1])
        pType2 = int(sys.argv[argpos + 2])
        player.append(Player(0, 0, pType1))
        player.append(Player(0, 1, pType2))
    else:
        player.append(Player(0, 0, 2))
        player.append(Player(0, 1, 2))

    fout = open("gamelog.json", "w+", encoding = 'utf-8')
    fout.write("{\n  \"step\" : [\n")

    Round = 0
    history = []

    while True:
        flag = False
        Round = Round + 1
        for i in range(board.playerNum):
            result = player[i].action(board, player[i ^ 1])
            if result['action']:
                flag = True
                history.append([i, result['tileType'], result['rotation'], 
                                result['flip'], result['x'], result['y']])
        if not flag:
            break
        else:
            print("Round %d: " % Round)
    
    for h in range(len(history)):
        curPlayer, tileType, rot, flp, x, y = history[h]
        fout.write('    {\n      "player" : %d,\n' % curPlayer)
        fout.write('      "action" : [\n')
        s = 0
        for (i, j) in shape.shapeSet[tileType][flp * 4 + rot]:
            fout.write('        { "row" : %d, "col" : %d}' % (x + i, y + j))
            s = s + 1
            if s != shape.tileSizes[tileType]:
                fout.write(',\n')
            else:
                fout.write('\n')
        fout.write('      ],\n      "state" : {}\n')
        if h != len(history) - 1:
            fout.write('    },\n')
        else:
            fout.write('    }\n')
    
    fout.write('  ]\n}\n')
    fout.close()

