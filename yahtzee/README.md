## Note
This program is a work in progress.

# Yahtzee Generator
A yahtzee generator calculates all possible die rolls given a set of die.
It will then provide the probability of scoring a box (assuming you know the rules of yahtzee) when the user enters a possible set of die.

### How are rolls done?
Rolls are done by calculating every possible set of die combinations and storing these combinations in a list.
Combinations are calculated using a recursive function.  A 5 digit number is incremented using this function, the digits can only be in range of 1 to 6.
There are 6^5 (7776) total possible combinations.  See help.txt for more information.  

### What is the logic behind rolling?
The number of total possible combinations is derived from the same logic we use when counting regular/decimal (base-10 aka 0 to 9) numbers and binary numbers (base-2 aka 0 to 1).  
Since there are 6 sides to a die, we will be counting in base-6 aka 1 to 6.  

When we count in base-10 we count from right to left; we count by increasing the right-most (least-significant) number until it reaches it's max value, which in base-10 is 9.
Then, we increase the next number to the left by one and we restart counting with the least-significant number.
When we count in base-2 we also count from right to left; we count the same way, increasing the right-most (least-significant) number/bit until it reaches it's max value, which in base-2 is 1.
The process is the same between each set, so the same logic can be applied to counting possible die aka base-6.

### Why 7776 total possible combinations?
The way we come upon 7776 is by a concept called positional notation.

TODO Explain this, I'm too lazy and tired rn lol

### How are probabilities calculated?
The program searches the list given a set of die and finds possible matches for every "score box" with the inputted set of die.
