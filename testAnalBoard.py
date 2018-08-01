from kernel import analBoard
from player import Player
from board import Board, Tiles

p1 = Player(0, 0, 0)
p2 = Player(0, 1, 0)
b = Board()

for i in range(5):
    p1.action(b, p2)
    p2.action(b, p1)

b.print()

res = analBoard(b, p1, p2)
def cmp(elem):
    return elem['winningRate']
res.sort(key = cmp, reverse = True)
for r in res:
    print("tile: %d, rot: %d, flip: %d, x: %d, y: %d, wr: %d%%" % (r['tileType'], r['rot'], r['flip'], r['x'], r['y'], r['winningRate'] * 100))
