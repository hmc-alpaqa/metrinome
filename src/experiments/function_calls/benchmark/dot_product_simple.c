#include <stdio.h>
#include <stdlib.h>

int
main(void)
{
        int a[3] = {1, 3, -5};
        int b[3] = {4, -2, -1};

        int sum = 0;
        size_t i;

        for (i = 0; i < sizeof(a) / sizeof(a[0]); i++) {
                sum += a[i] * b[i];
        }

        return sum;

        return EXIT_SUCCESS;
}