#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// int addition(int x, int y)
// {
//     return x + y;
// }

// int addition_wrapper(int x, int y)
// {
//     return addition(x,y);
// }

// int bad_addition(int x, int y)
// {
//     if (y > 0)
//     {
//         while (y != 0)
//         {
//             x = x + 1;
//             y = y - 1;

//         }
//     }
//     return x + y;
// }

// int worst_addition(int x, int y)
// {
//     int z = 0;
//     if (y > 0)
//     {
//         while (y != 0)
//         {
//             x = x + 1;
//             y = y - 1;

//         }
//         while (x != 0)
//         {
//             z = addition(2,1);
//         }
//     }
//     return x + y;
// }

// int one_loop(int x, int y)
// {
//     x = 1;
//     if (y > 0)
//     {
//         y = y + 1;
//         y = y - 1;
//     }
//     while (x > 0)
//     {
//         x = x - 1;
//     }
//     return x + y;
// }

int nested_loops(int x)
{
    x = 2;
    while (x > 0)
    {
        while (x > 1)
        {
            x = x - 1;
        }
        x = x - 1;
    }
    return x;
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

// TESTING BAD ADDITIONS

// int two_bad_addition(int x,int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     return x;
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

// int four_bad_addition(int x, int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
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

// int six_bad_addition(int x, int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     return x;
// }

// int seven_bad_addition(int x, int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     return x;
// }

// int eight_bad_addition(int x, int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     return x;
// }

// int nine_bad_addition(int x, int y)
// {
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     x = bad_addition(x,y);
//     return x;
// }

// int ten_bad_addition(int x, int y)
// {
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     bad_addition(2,1);
//     return x;
// }

// TESTING WITH NORMAL ADDITIONS

// int two_addition(int x, int y)
// {
//     x = addition(2,1);
//     x = addition(2,1);
//     return x;
// }

// int three_addition(int x, int y)
// {
//     x = addition(2,1);
//     x = addition(2,1);
//     x = addition(2,1);
//     return x;
// }


// TESTING WITH WRAPPERS 

// int two_addition_wrapper(int x, int y)
// {
//     x = addition_wrapper(2,1);
//     x = addition_wrapper(2,1);
//     return x;
// }

// // Can't compute??
// int three_addition_wrapper(int x, int y)
// {
//     x = addition_wrapper(2,1);
//     x = addition_wrapper(2,1);
//     x = addition_wrapper(2,1);
//     return x;
// }

// // Also can't compute
// int four_addition_wrapper(int x, int y)
// {
//     x = addition_wrapper(2,1);
//     x = addition_wrapper(2,1);
//     x = addition_wrapper(2,1);
//     x = addition_wrapper(2,1);
//     return x;
// }

// TESTING WORST ADDITION

// int two_worst_addition(int x, int y)
// {
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     return x;
// }

// int three_worst_addition(int x, int y)
// {
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     return x;
// }

// int four_worst_addition(int x, int y)
// {
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     return x;
// }

// int five_worst_addition(int x, int y)
// {
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     return x;
// }

// int six_worst_addition(int x, int y)
// {
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     x = worst_addition(2,1);
//     return x;
// }

// TESTING ONE LOOP

// int two_one_loop(int x, int y)
// {
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     return x;
// }

// int three_one_loop(int x, int y)
// {
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     return x;
// }

// int four_one_loop(int x, int y)
// {
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     return x;
// }

// int five_one_loop(int x, int y)
// {
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     x = one_loop(2,1);
//     return x;
// }

// TESTING NESTED LOOPS

int two_nested_loops(int x, int y)
{
    x = nested_loops(2);
    x = nested_loops(2);
    return x;
}

int three_nested_loops(int x, int y)
{
    x = nested_loops(2);
    x = nested_loops(2);
    x = nested_loops(2);
    return x;
}

int four_nested_loops(int x, int y)
{
    x = nested_loops(2);
    x = nested_loops(2);
    x = nested_loops(2);
    x = nested_loops(2);
    return x;
}