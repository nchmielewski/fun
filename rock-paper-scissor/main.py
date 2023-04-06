import random

def convert(s):
    if s == ('r' or 'rock' or 'R' or 'Rock'):
        return 'Rock'
    elif s == ('p' or 'paper' or 'P' or 'Paper'):
        return 'Paper'
    elif s == ('s' or 'scissors' or 'S' or 'Scissors'):
        return 'Scissors'
    
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

    com = random.choice(['Rock', 'Paper' ,'Scissors'])
    i = convert(i)
    
    if i == 'e':
        print('Not valid option!  Please enter r/R/rock/Rock or p/P/paper/Paper or s/S/scissors/Scissors')
        continue

    v = verdict(i, com)

    match v:
        case 0:
            print(f'{i} beats {v} - Player wins!')
            
        case 1:
            print(f'{v} beats {i} - Computer wins!')
            
        case 2:
            print(f'Both picked {i} - Tie!')
            



