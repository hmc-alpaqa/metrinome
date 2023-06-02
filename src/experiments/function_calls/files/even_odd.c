#include <stdbool.h>
int is_even(int n);
int is_odd(int n);

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

// int gcd(int a, int b)
// {
//     while (a != b)
//     {
//         if (a > b)
//         {
//             a = a - b;
//         }
//         else
//         {
//             b = b - a;
//         }
//     }
//     return a;
// }
