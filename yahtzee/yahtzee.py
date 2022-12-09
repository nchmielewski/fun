import math
import yahtzeehelper as yh

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

#   recursive function, init pass i=4 to aid recursion
def bhelp(n,i):     # init n=[0,0,0,0,0], i=4, func counts +1 given binary number list
    if i==-1:
        return 0    # overflow, done

    if n[i]==0:     # if current spot can be indented, indent and clear previous spots to 0
        if i==4:    # if first spot, no previous spots to clear
            n[i]=1
            return n
            
        n[i]=1
        for y in range(4,i,-1):
            n[y]=0
        return n 
        
    else:
        return bhelp(n,i-1)

#   recursive function, init pass i=4 to aid recursion
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

# all possible combinations of a given die
# dice provides the actual die set, L provides binary notation as to which indexes are to be rolled?
def roll(dice,L):

    # choosing will have separate func
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


# TODO create main for driver code
#driver

possibilities = []
die = [1, 1, 1, 1, 1]
while die != [6, 6, 6, 6, 6]:
    i = shelp(die, 4)
    print(die)
    possibilities.append(die)
print(possibilities)
# TODO figure out why the fuck possibilities is just [6, 6, 6, 6, 6]

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