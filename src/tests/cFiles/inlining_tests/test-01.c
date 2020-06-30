#include <stdio.h> 

int main() {
    // inline function call 
    int x = 0; 
    int y;
    int z;

    while (x < 23) {
        y = ++x;
        ++x;
    }
    z = x;

    return 0;
}