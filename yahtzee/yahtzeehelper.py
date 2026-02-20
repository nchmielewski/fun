

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
    unique_dice = set(dice)
    sequences = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})
    return 15 if any(seq.issubset(unique_dice) for seq in sequences) else 0


def LargeStraight(dice):
    unique_sorted = sorted(set(dice))
    return 20 if unique_sorted in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]) else 0


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
