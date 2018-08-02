
# game engine

from board import Tiles, Board
from player import Player
import shape
import sys
import time

if __name__ == '__main__':

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
        player.append(Player(0, 1, 0))
    
    evf = [0, 0]
    if '-e' in sys.argv[1:]:
        argpos = sys.argv.index('-e')
        evf[0] = int(sys.argv[argpos + 1])
        evf[1] = int(sys.argv[argpos + 2])

    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    fout = None

    if testMode:
        fout = open("game.out", "w+", encoding = 'utf-8')
        
    for g in range(50):
        player[0].clear()
        player[1].clear()
        board.clear()
        board.print(fout)
        Round = 0

        totSt = time.time()
        while True:
            flag = False
            Round = Round + 1
            for i in range(board.playerNum):
                startTime = time.time()

                result = player[i].action(board, player[i ^ 1], setEvalFunc = evf[i])
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
                    
                endTime = time.time()
                print("player %d: %s" % (i, endTime - startTime))
            if not flag:
                if testMode:
                    fout.write("\n")
                    for i in range(board.playerNum):
                        fout.write("player %d: %d\n" % (i, player[i].score))
                else:
                    print()
                    for i in range(board.playerNum):
                        print("player %d: %d" % (i, player[i].score))
                if player[0].score > player[1].score:
                    cnt1 += 1
                elif player[0].score == player[1].score:
                    cnt2 += 1
                else:
                    cnt3 += 1
                break
            else:
                print("Round %d: " % Round)
        
        totEd = time.time()
        print("tot time = %f" % (totEd - totSt))
    
    print("%d %d %d" % (cnt1, cnt2, cnt3))

    if testMode:
        fout.close()

