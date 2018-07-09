
# game engine

from board import Tiles, Board
from player import Player
import shape
import sys

argc = len(sys.argv)

testMode = False
if '-t' in sys.argv[1:]:
    testMode = True

board = Board()
player = []
if '-p' in sys.argv[1:]:
    argpos = sys.argv.index('-p')
    pType1 = int(sys.argv[argpos + 1])
    pType2 = int(sys.argv[argpos + 2])
    player.append(Player(0, 0, pType1))
    player.append(Player(0, 1, pType2))
else:
    player.append(Player(0, 0, 0))
    player.append(Player(0, 1, 2))

if __name__ == '__main__':

    if testMode:
        fout = open("game.out", "w+", encoding = 'utf-8')
        board.print(fout)

    Round = 0

    while True:
        flag = False
        Round = Round + 1
        for i in range(board.playerNum):
            result = player[i].action(board, player[i ^ 1])
            if result['action']:
                flag = True
                if testMode:
                    fout.write("player %d: %d %d %d %d %d\n"
                        % (i, result['tileType'], result['rotation'], result['flip'], 
                            result['x'], result['y']))
                    board.print(fout)
                else:
                    board.print()
                    print("%d\n" % i, end = '')
                    for coo in shape.shapeSet[result['tileType']][result['rotation'] + result['flip'] * 4]:
                        print("%d %d " % (result['x'] + coo[0], result['y'] + coo[1]), end = '')
                    print()
        if not flag:
            if testMode:
                fout.write("\n")
                for i in range(board.playerNum):
                    fout.write("player %d: %d\n" % (i, player[i].score))
            else:
                print()
                for i in range(board.playerNum):
                    print("player %d: %d" % (i, player[i].score))
            break
        else:
            print("Round %d: " % Round)
    
    if testMode:
        fout.close()

