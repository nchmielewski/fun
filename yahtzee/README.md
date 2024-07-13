## Note
This program is a work in progress.

# Yahtzee Generator
A yahtzee generator calculates all possible die rolls given a set of die.
It will then provide the probability of scoring a box (assuming you know the rules of yahtzee) when the user enters a possible set of die.

### How are rolls done?
There are 6^5 (7776) total possible combinations.

Calculating for every possible set of die combinations will give us a static number of rolls.  We store these combinations in a list and later check the list for possible points.
Combinations are calculated using a recursive function.  A 5 digit number is incremented using this function, the digits can only be in range of 1 to 6.
 
See help.txt for more information.  

### What is the logic behind rolling?
The number of total possible combinations is derived from the same logic we use when counting regular/decimal (base-10 aka 0 to 9) numbers and binary numbers (base-2 aka 0 to 1).  
Since there are 6 sides to a die, we will be counting in base-6 aka 1 to 6.  

When we count in base-10 we count from right to left; we count by increasing the right-most (least-significant) number until it reaches it's max value, which in base-10 is 9.
Then, we increase the next number to the left by one and we restart counting with the least-significant number.
When we count in base-2 we also count from right to left; we count the same way, increasing the right-most (least-significant) number/bit until it reaches it's max value, which in base-2 is 1.
The process is the same between each set, so the same logic can be applied to counting possible die aka base-6.

## Why 7776 total possible combinations?
##### Devs: It's just counting in binary, but replace the range of numbers to 0-5.

The way we come upon 7776 is by a concept called positional notation.  If you can count numbers, you intuitively already understand this concept.
There are two sets of numbers to consider: the range of numbers which are used (0-9 for base-10, 0-1 for base-2) and the position of the left-most/greatest/most-significant digit.

Positional notation can be calculated by a simple base and exponent, where the range (R) is the base number and the position (P) is the exponent: R ^ P
With this equation, we can calulate the number of possible combinations.  Let me provide some examples.

#### Base-10 Example
Let's say we want to find out the total possible combinations for a single base-10 digit.  That is, how many numbers can you have with a single digit which can range from 0 to 9?  You already intuitively know the answer, it's 10.  
To be crude and count it out: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9
For a single base-10 digit the equation is: 10^1 = 10

Now let's find the total possible combinations of numbers using two base-10 digits.  How many numbers can you have with two digits which each can range from 0 to 9?
To be crude: 00 -> 01 -> 02 ... 09 -> 10 -> 11 ... 19 -> 20 -> 21 ... 29 -> 30 -> 31 ... 89 -> 90 -> 91 ... 97 -> 98 -> 99
The answer is 100.  The equation is: 10^2 = 100

Now if we were to find the total possible combinations for three base-10 digits, you may already derive it's 1000 as 10^3 = 1000.

#### Base-2 Example
Let's change it up, say we want to find the total possible combinations for a single base-2 digit. This may be easy, it's the number you can have with a single digit which can range from 0 to 1, it's 2.
Let's be crude: 0 -> 1
The equation is 2^1 = 2.

What about for two base-2 digits?  Let's be crude: 00 -> 01 -> 10 -> 11
The answer is 4, the equation is: 2^2 = 4

One last example, what about three base-3 digits?
Crude way: 000 -> 001 -> 010 -> 011 -> 100 -> 101 -> 110 -> 111
The answer is 8: 2^3 = 8

There comes a point where counting no longer helps, this is where the equation shines.  What if we have 64 base-2 digits?  
2^64 = 1.8446744e+19
That's a lot of bits, it's 2,305,843 terabytes!  Great googly moogly!

#### Base-6 Example
Now we come to how this is useful in the case of rolling die, and how I came up with 7776 possible combinations.  I'll assume you got the hang of the equation by now.

One die, a single base-6 digit: 6^1 = 6

Two die?  6^2 = 36

What if we have five die (like in Yahtzee!)?  6^5 = 7776

##### For more information, check out this wiki page: https://en.wikipedia.org/wiki/Positional_notation

### How are probabilities calculated?
The program searches the list given a set of die and finds possible matches for every "score box" with the inputted set of die.
