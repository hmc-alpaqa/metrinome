#include <stdio.h>
#include <stdlib.h>

int
dot_product(int *a, int *b, size_t n)
{
        int sum = 0;
        size_t i;

        for (i = 0; i < n; i++) {
                sum += a[i] * b[i];
        }

        return sum;
}
