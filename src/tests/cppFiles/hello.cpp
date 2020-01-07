/* hello.cpp */
#include <iostream>
using namespace std;
int main()
{
    cout << "Please enter your name: ";
    string name;
    cin >> name;
    cout << "Hello, " << name;
    if (name != ":^)") {
        for (int i = 0; i < 100; ++i) {
            if (i == name.size()) {
                return 5;
            }
        }
    }
    cout << "\n";
    return 5;
} 
