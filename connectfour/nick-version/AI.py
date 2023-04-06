import board as B

class AI:
    def __init__(self):
            self.board = B.Board()

    def updateBoard

    def placeTokenAI(self):
        pass

    def checkForRuns(self):     # checks for potential dubs, returns the number of total tokens in dub
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

        elif self.board.get((x, y)) is not main.OGV:    # if coord vacant, off board, or opposing side, end count
            print('OGV = ', main.OGV, '\n', 'self.board.get((x, y) = ', self.board.get((x, y)))
            print('Failed.')
            return connect

        else:                                           # if no connect 4 and matching token, count matched token
            connect += 1
            x, y = l[toggle]                            # using toggle, reassign x and y to new coordinates
            self.check(x, y, connect, toggle)           # recursive call
        print('nothing happened')
