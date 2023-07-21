#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

string convert(string x){
  if (x == "rock" || x == "Rock" || x == "r" || x == "R") {
    return "r";
  }
  else if (x == "paper" || x == "Paper" || x == "p" || x == "P") {
    return "p";
  }
  else if (x == "scissors" || x == "Scissors" || x == "s" || x == "S") {
    return "s";
  }
  else if (x == "quit" || x == "Quit" || x == "q" || x == "Q") {
    return "q";
  }
  else return "e";
}

int decide(int AI, string x) {
  string player = convert(x);
  
  switch(AI):
    case 0:
      cout << "Computer picked rock" << endl;
      if (x == "p")
    case 1:
      cout << "Computer picked paper" << endl;
    case 2:
      cout << "Computer picked scissors" << endl;
}

int main() {
  string x; 
  cout << "Let's play rock paper scissors.  The computer will randomly pick an option." << "\n";
  
  bool running = true;
  while (running) {
    cout << "Enter your choice: " << x << endl;
    cin >> x; // Get user input from the keyboard
    
    int AI = rand() % 3;    // 0 rock, 1 paper, 2 scissors
    
    bool result = decide(AI, x);

    if result{ return 0 }
    
  }
  
}
