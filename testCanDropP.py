# test for Board.canDropPos
from board import Tiles, Board
from player import Player
import numpy as np 

board = Board()
player = Player(0, 0, -1)

board.board[3][3] = 1
board.board[4][4] = 1
tile = Tiles(17, 0, 0)

ret = board.canDropPos(player, tile)
print(ret)

print(board.getCorners(player)[0].size)
