# horses
Program to calculate and maintain a database of stats of minecraft horses.
By using this tool, we can better manage stats of the herd to create the most perfect horse possible.

### How is this done?
The stats of a horse can be measured in game based on how many hearts it has, how high it can jump, and how fast it can run.
A horse can be a randomly generated mob or bred by two horses into a foal (baby horse :D).

The stats of a foal is calculated in game using a simple equation, where it utilizes the stats of the parents and the stats of a randomly generated horse.
The foal inherits some of the parents' traits, but it mutates via the random stats.
Let F be the stats of the foal, Pa be the stats of parent A, Pb be the stats of parent B, and R be the stats of the random stats:
F = (Pa + Pb)/3 + R/3

By measuring the stats of the foal we can determing the random stats R.  In this way, we can determine if the random stats were high or low.
If the stats are high, this foal will be a promising future breeder as RNJesus has blessed us with a good roll.
If the stats are low, this foal is kinda dead weight and not fruitful progression for the herd to the most perfect horse and we could cull the foal (baby horse D:).