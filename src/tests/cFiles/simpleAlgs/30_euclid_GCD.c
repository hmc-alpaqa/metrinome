#include <stdio.h>

int gcd(int a, int b) {
    while (a != b) {
        if (a > b) {
            a = a - b;
        } else {
            b = b - a;
        }
    }
    return a;
}

int main() {
    int a = 24;
    int b = 18;
    int result = gcd(a, b); 
    printf("%d\n", result);
}
