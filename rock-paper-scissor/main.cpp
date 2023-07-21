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

// return 0/nothing 1/player 2/pc
int decide(int AI, string x) {

  switch(AI):
    case 0:
      cout << "Computer picked rock" << endl;
      if (x == "p") return 1;
      elif (x == "s") return 2;
      else return 0;
    case 1:
      cout << "Computer picked paper" << endl;
      if (x == "s") return 1;
      elif (x == "r") return 2;
      else return 0;
    case 2:
      cout << "Computer picked scissors" << endl;
      if (x == "r") return 1;
      elif (x == "p") return 2;
      else return 0;
}

int main() {
  string x; 
  cout << "Let's play rock paper scissors.  The computer will randomly pick an option." << "\n";
  
  bool running = true;
  while (running) {
    cout << "Enter your choice: " << x << endl;
    cin >> x; // Get user input from the keyboard
    
    string player;
    if (convert(x) == "e") {
      cout << "Please type normally" << endl;
      continue;
    }
    elif (convert(x) == "normally") {
      cout << "Alright wise guy, haha!" << endl;
    }

    int AI = rand() % 3;    // 0 rock, 1 paper, 2 scissors
    
    bool result = decide(AI, player);

    if result{ return 0 }
    
  }
  
}
