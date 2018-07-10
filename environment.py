
# environment

from board import Tiles, Board
from player import Player
import shape
import sys

if __name__ == '__main__':

    argc = len(sys.argv)

    player = []

    '''
        -s x: the player #x will go first
        default x = 0
    '''
    sente = 0
    if '-s' in sys.argv[1:]:
        argpos = sys.argv.index('-s')
        sente = sys.argv[argpos + 1] % 2

    '''
        -p level: pvc mode. Human player is player #0,
            and 'level' is the level of AI
        or
        -c level1 level2: cvc mode. 
            'level1' and 'level2' are the levels of 
            player #0 and player #1 represently
        default: -c 0 0

        -p and -c can not be set simutaneously, 
        or an exception will be thrown
    '''
    if '-p' in sys.argv[1:]:
        if '-c' in sys.argv[1:]:
            raise Exception("config conflict: [-p, -c]")
        argpos = sys.argv.index('-p')
        pType = int(sys.argv[argpos + 1])
        
        player.append(Player(0, sente, -1))
        player.append(Player(0, sente ^ 1, pType))
    elif '-c' in sys.argv[1:]:
        argpos = sys.argv.index('c')
        pType = [int(sys.argv[argpos + i]) for i in range(2)]
        player.append(Player(0, sente, pType[0]))
        player.append(Player(0, sente ^ 1, pType[1]))
    else:
        player.append(Player(0, sente, 0))
        player.append(Player(0, sente ^ 1, 0))

    board = Board()

    while True:
        playerOrder, tileSize = list(map(int, input().split(' ')))
        playerOrder = playerOrder ^ sente
        tile = []
        minx = 14
        miny = 14
        for i in range(tileSize):
            x, y = list(map(int, input().split(' ')))
            tile.append([x, y])
            minx = min(minx, x)
            miny = min(miny, y)
        result = board.dropTile(playerOrder, tile)
        if result:
            for i in range(tileSize):
                tile[i][0] -= minx
                tile[i][1] -= miny
            tile.sort()
            for t in range(21):
                if shape.tileSizes[t] != tileSize:
                    continue
                if tile in shape.shapeSet[t]:
                    player[playerOrder].used[t] = True
                    break
            player[playerOrder].score += tileSize
            if board.isOver(player):
                print("-1")
                print("%d %d " % (player[0].score, player[1].score))
                break
            else:
                print(playerOrder ^ 1)
                print(tileSize)
                for i in range(tileSize):
                    print("%d %d " % (tile[i][0] + minx, tile[i][1] + miny))
                board.print()
        else:
            print("-2")
            break

