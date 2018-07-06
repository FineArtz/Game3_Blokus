
# game engine

from board import Tiles, Board
from player import Player

board = Board()
player = []
player.append(Player(0, 0, 0))
player.append(Player(0, 1, 1))

if __name__ == '__main__':

    fout = open("game.out", "w+", encoding = 'utf-8')
    board.print(fout)

    Round = 0

    while True:
        flag = False
        Round = Round + 1
        for i in range(board.playerNum):
            result = player[i].action(board)
            if result['action']:
                flag = True
                fout.write("player %d: %d %d %d %d %d\n"
                    % (i, result['tileType'], result['rotation'], result['flip'], 
                        result['x'], result['y']))
                board.print(fout)
        if not flag:
            fout.write("\n")
            for i in range(board.playerNum):
                fout.write("player %d: %d\n" % (i, player[i].score))
            break
        else:
            print("Round %d: " % Round)
    
    fout.close()

