import AI as A
import board as B

class ConnectFour():
    def __init__(self):
        self.game = B.Board()
        self.turn = True    # True/Player  False/PC
        self.OGV = 0
        self.score = '0/0/0'

    def createBoard(self):              # creates board for the first time
        for y in range(1, 7):
            for x in range(1, 8):
                self.game.board.update({(x, y): 0})
        print(self.game.board)

    # TODO make sure this runs with new classes
    def run(self):
        self.createBoard()              # on start up, create a new board
        while True:                     # runs until checkFor4 returns 1
            if self.turn is True:       # if player turn, else PC turn
                val = input("Enter coordinate: ")
                self.game.placeToken(val)
            else:
                A.placeTokenAI(self)

            # after a turn is played, we check for dubs
            if self.game.checkFor4() == 0:                       # if no connect 4, continue w/ while loop
                self.turn = not self.turn                   # switch next turn
            else:                                           # if connect 4, break while loop
                break

        # declare winner
        print("///////   GAME OVER   ///////", '\n', "Winner: ", 'Player' if self.turn == True else 'Computer')
        self.game.board.printBoard()