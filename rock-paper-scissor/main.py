import random

def convert(s):
    if s == ('r' or 'rock' or 'R' or 'Rock'):
        return 'r'
    elif s == ('p' or 'paper' or 'P' or 'Paper'):
        return 'r'
    elif s == ('s' or 'scissors' or 'S' or 'Scissors'):
        return 's'
    
    else: return 'e'

# return: 0 player, 1 computer, 2 tie
def verdict(i, com):
    if i == com:
        return 2


#driver
score = '0 - 0 - 0'
while True:
    print("Let's play rock paper scissors.  The computer will randomly pick an option.", '\n', "Enter your choice: ")
    i = input()

    com = random.choice(['r', 'p' ,'s'])
    i = convert(i)
    v = verdict(i, com)

    match v:
        case 0:
            print(f'{i} beats {v} - Player wins!')
            score[0] = str(int(score[0]) + 1)
        case 1:
            print(f'{v} beats {i} - Computer wins!')
            score[8] = str(int(score[8]) + 1)
        case 2:
            print(f'Both picked {i} - Tie!')
            score[4] = str(int(score[4]) + 1)



