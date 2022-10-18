import math
import unittest
    
#helpers
def HighestRepeated(dice, minRepeats):
    unique = set(dice)
    repeats = [x for x in unique if dice.count(x) >= minRepeats]
    return max(repeats) if repeats else 0

def OfAKind(dice, n):
    return HighestRepeated(dice,n) * n

def SumOfSingle(dice, selected):
    return dice.count(selected) * selected

#strategies
def Chance(dice):
    return sum(dice)

def Pair(dice):
    return OfAKind(dice, 2)

def ThreeOfAKind(dice):
    return OfAKind(dice, 3)

def FourOfAKind(dice):
    return OfAKind(dice, 4)

def SmallStraight(dice):
    ctr=0
    for x in dice:
        #if not in sequence, new x
        pass
        #if next, index ctr
        
    dice = tuple(dict.fromkeys(dice)) #  removes duplicates
    return 15 if sorted(dice) == (1, 2, 3, 4)or(2, 3, 4, 5)or (3, 4, 5, 6) else 0

def LargeStraight(dice):
    return 20 if sorted(dice) == (1, 2, 3, 4, 5) or (2, 3, 4, 5, 6) else 0

def Ones(dice):
    return SumOfSingle(dice,1)

def Twos(dice):
    return SumOfSingle(dice,2)

def Threes(dice):
    return SumOfSingle(dice,3)

def Fours(dice):
    return SumOfSingle(dice,4)

def Fives(dice):
    return SumOfSingle(dice,5)

def Sixes(dice):
    return SumOfSingle(dice,6)

def Yahtzee(dice):
    return 50 if len(dice) == 5 and len(set(dice)) == 1 else 0

def poss():
    L=[]
    s=[1, 1, 1, 1, 1]
    for x in range(1, 7):
        for y in range(1, 7):
            pass
    return L

def bin():
    s=[0,0,0]
        
    while s!=[1,1,1]:
        pass

def bhelp(n,i): # init n=[0,0,0,0,0], i=4, func counts +1 given binary number list
    if i==-1:
        return 0   # overflow

    if n[i]==0: #if current spot can be indented, indent and clear previous spots to 0
        if i==4:#if first spot, no previous spots to clear
            n[i]=1
            return n
            
        n[i]=1
        for y in range(4,i,-1):
            n[y]=0
        return n 
        
    else:
        return bhelp(n,i-1)

def shelp(n,i):
    #overflow
    if i==-1:
        return 0
        
    # if current spot can be indented, indent and clear previous spots to 1
    if n[i]==1 or n[i]==2 or n[i]==3 or n[i]==4 or n[i]==5:
        # if first spot, no previous spots to clear
        if i==4:
            n[i]+=1
            return n
            
        n[i]+=1
        for y in range(4,i,-1):
            n[y]=1
        return n
        
    # else recurse to next bit
    else:
        return shelp(n,i-1)
    
def roll(dice,L):#all possible combinations of a given die
    #chose 1
    #alternate between bits
    for x in L:
        pass

    #chose 2
        #double for loop

    #chose 3
        #triple for loop
    

    #chose 4
        #quad loop

    #choose 5
        #all 5
            
def check(dice, roll):
    #check for next roll
    pass
    #check for two rolls ahead (if first roll)

#driver
"""
L=[]
y = [1,1,1,1,1]
yy=y
L.append(yy)
print(L)
ctr=1
while y!=[1,1,1,1,6]:
    print("1L =",L)
    ctr+=1
    y = shelp(y, 4)
    yy=y
    L.append(yy)
    print("2L =",L)
print(ctr)
print(L)

while False:
    v = tuple(input("First Roll\nEnter die: "))
    print(v)
        
    v = tuple(input("Second Roll\nEnter die: "))
    print(v)
"""
print(bhelp([0,0,0,0,0], 4))
