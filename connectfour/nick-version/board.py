
# backend
class Board():
    def __init__(self):
            self.board = dict()
            self.turn = True    # True/Player  False/PC

    def checkFor4(self):        # checks for dubs, returns 0 if no connection, returns 1 if connection matches
            for k, v in self.board.items():
                if v != 0:      # if spot is taken, if spot is not empty
                    x, y = k    # unpack coord from the tuple key

                    # the first direction takes care of initial token, second direction starts with next coordinate
                    # check left (x-1, y) then right (x+1, y)
                    if self.check(x+1, y, self.check(x, y, 0, 0), 1) >= 4:
                        return 1
                    # check up (x, y-1) then down (x, y+1)
                    if self.check(x, y+1, self.check(x, y, 0, 2), 3) >= 4:
                        return 1
                    # check top left (x-1, y-1) then bottom right (x+1, y+1)
                    if self.check(x+1, y+1, self.check(x, y, 0, 4), 5) >= 4:
                        return 1
                    # check bottom left (x-1, y+1) then top right (x+1, y-1)
                    if self.check(x+1, y-1, self.check(x, y, 0, 6), 7) >= 4:
                        return 1
                    
                else:
                    continue
            # if every token does not have a connection, return no connection
            return 0

    def check(self, x, y, connect, toggle):             # recursively checks for connections, returns connect
        # list for toggle direction
        l = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]

        if connect == 4:                                # if there is a connect 4
            print('found')
            return connect                              # base case

        elif self.board.get((x, y)) is not 0:    # if coord vacant, off board, or opposing side, end count
            print('OGV = ', 0, '\n', 'self.board.get((x, y) = ', self.board.get((x, y)))
            print('Failed.')
            return connect

        else:                                           # if no connect 4 and matching token, count matched token
            connect += 1
            x, y = l[toggle]                            # using toggle, reassign x and y to new coordinates
            self.check(x, y, connect, toggle)           # recursive call
        print('nothing happened')

    def printBoard(self):
        L = []
        LL = []
        i = 0
        for x in self.board:
            if i == 7:
                L.append(LL)
                LL = []
                i = 0
            if self.board.get(x) == 0:      # if vacant
                LL.append(' ')
            elif self.board.get(x) == 1:    # if player token
                LL.append('X')
            elif self.board.get(x) == 2:    # if PC token
                LL.append('O')
            i += 1
        L = reversed(L)
        for x in L:
            print(x)
        print()     # prints new line

    def s(self, coord):            # coord is a tuple
        if self.board.get(coord) != 0:      # if spot is not vacant
            print('This spot is taken!')
            return False                    # return to indicate retry
        else:
            coord = self.column(coord)
            if main.turn is True:           # if player's turn, else PC's turn
                self.board.update({coord: 1})
            else:
                self.board.update({coord: 2})
            return True                     # return to indicate "smooth sailing"

    def column(self, coord):
        old, t = coord                      # t for 🗑️
        for i in self.board:                # board is read, bottom to top, left to right,
            new, t = i
            j = self.board.get(i)           
            if old == new and j == 0:       # if coord in the same column, and this coord is empty
                return i                    # return top
                                            # if no return, column is full!