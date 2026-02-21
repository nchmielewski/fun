

# helpers
def HighestRepeated(dice, minRepeats):
    unique = set(dice)
    repeats = [x for x in unique if dice.count(x) >= minRepeats]
    return max(repeats) if repeats else 0


def OfAKind(dice, n):
    return HighestRepeated(dice, n) * n


def SumOfSingle(dice, selected):
    return dice.count(selected) * selected


# strategies
def Chance(dice):
    return sum(dice)


def Pair(dice):
    return OfAKind(dice, 2)


def ThreeOfAKind(dice):
    return OfAKind(dice, 3)


def FourOfAKind(dice):
    return OfAKind(dice, 4)


# TODO complete logic
def SmallStraight(dice):
    ctr = 0
    for x in dice:
        # if not in sequence, new x
        pass
        # if next, index ctr

    dice = tuple(dict.fromkeys(dice))  # removes duplicates
    return 15 if sorted(dice) == (1, 2, 3, 4) or (2, 3, 4, 5) or (3, 4, 5, 6) else 0


def LargeStraight(dice):
    return 20 if sorted(dice) == (1, 2, 3, 4, 5) or (2, 3, 4, 5, 6) else 0


def Ones(dice):
    return SumOfSingle(dice, 1)


def Twos(dice):
    return SumOfSingle(dice, 2)


def Threes(dice):
    return SumOfSingle(dice, 3)


def Fours(dice):
    return SumOfSingle(dice, 4)


def Fives(dice):
    return SumOfSingle(dice, 5)


def Sixes(dice):
    return SumOfSingle(dice, 6)


def Yahtzee(dice):
    return 50 if len(dice) == 5 and len(set(dice)) == 1 else 0