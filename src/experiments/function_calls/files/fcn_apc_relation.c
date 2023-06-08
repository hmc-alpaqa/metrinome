#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// int addition(int x, int y)
// {
//     return x + y;
// }

int bad_addition(int x, int y)
{
    if (y > 0)
    {
        while (y != 0)
        {
            x = x + 1;
            y = y - 1;

        }
    }
    return x + y;
}

// int impossible_call(int x)
// {
//     if (x > 10 && x < 5)
//     {
//         //return x + 1;
//         return bad_addition(x,x);
//     }
//     return 1;
// }

// int possible_call(int x)
// {
//     if (x > 10 && x < 15)
//     {
//         return bad_addition(x,x);
//     }
//     return 1;
// }

// int three_bad_addition(int x, int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     return x;
// }

// int other_three_bad_addition(int x)
// {
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     return x;
// }

// int five_bad_addition(int x, int y)
// {
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     return x;
// }

int ten_bad_addition(int x, int y)
{
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    bad_addition(2,1);
    return x;
}


// int again_three_bad_addition(int x)
// {

// }