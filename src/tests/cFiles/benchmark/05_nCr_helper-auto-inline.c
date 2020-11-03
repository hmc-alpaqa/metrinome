#include <stdio.h>

__attribute__((always_inline)) inline int factorial(int);
__attribute__((always_inline)) inline int combination(int, int);

int main()
{
    int n, r, c;
    printf("Enter the value of n :");
    scanf("%d", &n);

    printf("Enter the value of r :");
    scanf("%d", &r);

    c = combination(n, r);

    printf("\nCombinations : %d", c);

    return 0;
}

__attribute__((always_inline)) inline int combination(int n, int r)
{
    int c;

    c = factorial(n) / (factorial(r) * factorial(n - r));

    return c;
}

__attribute__((always_inline)) inline int factorial(int n)
{
    int i;
    int fact = 1;

    for (i = 1; i <= n; i++)
    {
        fact = fact * i;
    }
    return fact;
}
