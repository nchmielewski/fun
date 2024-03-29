import random

def convert(s):
    if s == 'r' or s == 'rock' or s == 'R' or s == 'Rock':
        return 'Rock'
    elif s == 'p' or s == 'paper' or s == 'P' or s == 'Paper':
        return 'Paper'
    elif s == 's' or s == 'scissors' or s == 'S' or s == 'Scissors':
        return 'Scissors'
    
    else: return 'e'

# return: 0 player, 1 computer, 2 tie
def verdict(i, com):
    if i == com:
        return 2
    
    match i:
        case 'Rock':
            if com == 'Scissors': return 0
            else: return 1

        case 'Paper':
            if com == 'Rock': return 0
            else: return 1

        case 'Scissors':
            if com == 'Paper': return 0
            else: return 1

#driver
score = [0, 0, 0]
print("Let's play rock paper scissors.  The computer will randomly pick an option.", '\n')
while True:
    i = input("Enter your choice: ")

    com = random.choice(['Rock', 'Paper', 'Scissors'])
    i = convert(i)
    
    if i == 'e':
        print('Not valid option!  Please enter r/R/rock/Rock or p/P/paper/Paper or s/S/scissors/Scissors')
        continue

    v = verdict(i, com)

    match v:
        case 0:
            print(f'{i} beats {com} - Player wins!')
            score[0] += 1
            
        case 1:
            print(f'{com} beats {i} - Computer wins!')
            score[1] += 1
            
        case 2:
            print(f'Both picked {i} - Tie!')
            score[2] += 1    
    
    print(f'Player won {score[0]}   Computer won {score[1]}   {score[2]} Ties', '\n')  
              



