## Note
This program is a work in progress.

# Yahtzee Generator
A yahtzee generator calculates all possible die rolls given a set of die.
It will then provide the probability of scoring a box (assuming you know the rules of yahtzee) when the user enters a possible set of die.

### How are rolls done?
Rolls are done by calculating every possible set of die combinations and storing these combinations in a list.
Combinations are calculated using a recursive function.  A 5 digit number is incremented using this function, the digits can only be in range of 1 to 6.
There are 6^5 (7776) total possible combinations.  See help.txt for more information.  You can ask Nick for an explanation for why the total is 6^5 ;) better to show than to type.

### How are probabilities calculated?
The program searches the list given a set of die and finds possible matches for every "score box" with the inputted set of die.
