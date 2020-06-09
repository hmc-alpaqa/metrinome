// https://computerscience4beginers.com/2016/10/26/recursive-and-non-recursive-functions-to-find-gcdhcf-of-a-two-numbers/

#include <stdio.h>

int hcf(int a, int b) {
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
    int result = hcf(a, b);  // 6
}
