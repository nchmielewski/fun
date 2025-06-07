#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    vector<string> msg {"hello", "world!"};

    for (auto x : msg) {
        cout << x << " ";
    }

    while (true) {
        cout << "\n" << "rah!";
    }
}
