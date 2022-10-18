from connectfour2 import ConnectFour

c4 = ConnectFour()
c4.createBoard()
c4.printBoard()
c4.placeToken((1, 1))
c4.turn = False
c4.placeToken((1, 2))
c4.placeToken((2, 2))
c4.placeToken((3, 2))
c4.placeToken((4, 2))
c4.printBoard()
c4.OGV = c4.board.get(4, 2)
print(c4.check(4, 2, 0, 0))