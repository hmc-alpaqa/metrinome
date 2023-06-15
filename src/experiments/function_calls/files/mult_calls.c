#include <stdbool.h>

bool givetrue(int a);


bool caller(int a)
{
    return givetrue(a) && givetrue(a);
}


bool givetrue(int a) {
    return true;
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