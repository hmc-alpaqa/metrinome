#include <stdbool.h>
#include "is_even.h"

int is_odd(int n)
{
    if (n == 0)
    {
        return 0;
    }
    else
    {
        return is_even(n - 1);
    }
}