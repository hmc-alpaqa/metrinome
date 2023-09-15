#include <stdio.h>
#include <stdlib.h>

int collatz(int n) {
    if (n == 1) {
        return 1;
    } else if (n % 2 == 0) {
        return collatz(n / 2);
    } else {
        return collatz(3 * n + 1);
    }
}

int inorder_mock(int n) {
    if (n == 1) {
        inorder_mock(2);
        n += 1;
        inorder_mock(2);
    } 
}

int main() {
    collatz(10);
    inorder_mock(1);
    inorder_mock(1);
}