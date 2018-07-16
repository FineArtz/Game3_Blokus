from board import Board, Tiles
from player import Player

if __name__ == '__main__':
    bd = Board()
    player = Player(0, 0, 0)
    opponent = Player(0, 1, 0)
    fin = open('parser.in', "r+")
    matrix = []
    str = fin.read().split('\n')
    for i in range(14):
        matrix.append(list(map(int, str[i].split(' '))))
    print(matrix)
    bd.parseFromMatrix(matrix, [player, opponent])
    print(player.used)
    print(opponent.used)
    print(player.corners)
    print(opponent.corners)
    fin.close()
