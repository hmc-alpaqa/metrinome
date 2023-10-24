#include <stdbool.h>
#include "is_odd.h"
#include <stdio.h>

int is_even(int n)
{
    if (n == 0)
    {
        return 1;
    }
    else
    {
        return is_odd(n - 1);
    }
}

// int main()
// {
//     int n = 8;
//     int result = is_even(n);
//     printf("Result: %d\n", result);
//     return 0;
// }