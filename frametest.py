
# test of tiles and board

import unittest
from board import Tiles

class TilesTest(unittest.TestCase):
    def test_rotate(self):
        fout = open("testRotate.out", "w+")
        tiles = []
        for i in range(21):
            tiles.append(Tiles(i))
        for i in range(21):
            fout.write("type %d\n" % i)
            for r in range(4):
                tiles[i].print(fout)
                fout.write("\n")
                tiles[i].rightRotate()
            tiles[i].horFlip()
            for r in range(4):
                tiles[i].print(fout)
                fout.write("\n")
                tiles[i].rightRotate()
            fout.write("\n")
        fout.close()

    def test_flip(self):
        fout = open("testFlip.out", "w+")
        tiles = []
        for i in range(21):
            tiles.append(Tiles(i))
        for i in range(21):
            fout.write("type %d\n" % i)
            tiles[i].print(fout)
            fout.write("\n")
            tiles[i].rightRotate()
            tiles[i].print(fout)
            fout.write("\n")
            tiles[i].horFlip()
            tiles[i].print(fout)
            fout.write("\n")
            tiles[i].verFlip()
            tiles[i].print(fout)
            fout.write("\n\n")
        fout.close()

    def __printTileAll(self, tile, fout):
        bd = []
        for i in range(9):
            bd.append([])
            for j in range(9):
                bd[i].append('-')
        for coo in tile.shape:
            bd[2 + coo[0]][2 + coo[1]] = '+'
        for coo in tile.corner:
            bd[2 + coo[0]][2 + coo[1]] = '*'
        for i in range(9):
            for j in range(9):
                fout.write(bd[i][j])
            fout.write("\n")
        fout.write("\n")

    def test_corner(self):
        fout = open("testCorner.out", "w+")
        tiles = []
        for i in range(21):
            tiles.append(Tiles(i))
        for i in range(21):
            fout.write("type %d\n" % i)
            for r in range(4):
                self.__printTileAll(tiles[i], fout)
                tiles[i].rightRotate()
            tiles[i].horFlip()
            for r in range(4):
                self.__printTileAll(tiles[i], fout)
                tiles[i].rightRotate()
            fout.write("\n")

if __name__ == '__main__':
    unittest.main()

