// copied from experiments/recursion/files/fibonacci_test.c
#include <stdio.h>

int linear_search_rec(int A[], int n, int x);

int linear_search_rec(int A[], int n, int x)
{
    if (n == 0) {
        return 0;
    } else if (A[0] == x) {
        return 1;
    } else {
        return linear_search_rec(A + 1, n - 1, x);
    }
}