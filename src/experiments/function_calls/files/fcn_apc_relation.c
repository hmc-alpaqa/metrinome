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

//sed to be call super_nested_loops
// int triple_nested_loops(int x)
// {
//     x = 3;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;    
// }

// int quadruple_nested_loops(int x)
// {
//     x = 4;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     x = x -1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;    
// }

// int quintuple_nested_loops(int x)
// {
//     x = 5;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

// int sextuple_nested_loops(int x)
// {
//     x = 6;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

// int septuple_nested_loops(int x)
// {
//     x = 7;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

// int octuple_nested_loops(int x)
// {
//     x = 8;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 while (x > 7)
//                                 {
//                                     x = x - 1;
//                                 }
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

// int nonuple_nested_loops(int x)
// {
//     x = 9;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 while (x > 7)
//                                 {
//                                     while (x > 8)
//                                     {
//                                         x = x - 1;
//                                     }
//                                     x = x - 1;
//                                 }
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

int decuple_nested_loops(int x)
{
    x = 10;
    while (x > 0)
    {
        while (x > 1)
        {
            while (x > 2)
            {
                while (x > 3)
                {
                    while (x > 4)
                    {
                        while (x > 5)
                        {
                            while (x > 6)
                            {
                                while (x > 7)
                                {
                                    while (x > 8)
                                    {
                                        while (x > 9)
                                        {
                                            x = x - 1;
                                        }
                                        x = x - 1;
                                    }
                                    x = x - 1;
                                }
                                x = x - 1;
                            }
                            x = x - 1;
                        }
                        x = x - 1;
                    }
                    x = x - 1;
                }
                x = x - 1;
            }
            x = x - 1;
        }
        x = x - 1;
    }
    return x;  
}

// int vigintuple_nested_loops(int x)
// {
//     x = 20;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 while (x > 7)
//                                 {
//                                     while (x > 8)
//                                     {
//                                         while (x > 9)
//                                         {
//                                             while (x > 10)
//                                                 {
//                                                     while (x > 11)
//                                                     {
//                                                         while (x > 12)
//                                                         {
//                                                             while (x > 13)
//                                                             {
//                                                                 while (x > 14)
//                                                                 {
//                                                                     while (x > 15)
//                                                                     {
//                                                                         while (x > 16)
//                                                                         {
//                                                                             while (x > 17)
//                                                                             {
//                                                                                 while (x > 18)
//                                                                                 {
//                                                                                     while (x > 19)
//                                                                                     {
//                                                                                         x = x - 1;
//                                                                                     }
//                                                                                     x = x - 1;
//                                                                                 }
//                                                                                 x = x - 1;
//                                                                             }
//                                                                             x = x - 1;
//                                                                         }
//                                                                         x = x - 1;
//                                                                     }
//                                                                     x = x - 1;
//                                                                 }
//                                                                 x = x - 1;
//                                                             }
//                                                             x = x - 1;
//                                                         }
//                                                         x = x - 1;
//                                                     }
//                                                     x = x - 1;
//                                                 }
//                                             x = x - 1;
//                                         }
//                                         x = x - 1;
//                                     }
//                                     x = x - 1;
//                                 }
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

int trigintuple_nested_loops(int x)
{
    x = 20;
    while (x > 0)
    {
        while (x > 1)
        {
            while (x > 2)
            {
                while (x > 3)
                {
                    while (x > 4)
                    {
                        while (x > 5)
                        {
                            while (x > 6)
                            {
                                while (x > 7)
                                {
                                    while (x > 8)
                                    {
                                        while (x > 9)
                                        {
                                            while (x > 10)
                                                {
                                                    while (x > 11)
                                                    {
                                                        while (x > 12)
                                                        {
                                                            while (x > 13)
                                                            {
                                                                while (x > 14)
                                                                {
                                                                    while (x > 15)
                                                                    {
                                                                        while (x > 16)
                                                                        {
                                                                            while (x > 17)
                                                                            {
                                                                                while (x > 18)
                                                                                {
                                                                                    while (x > 19)
                                                                                    {
                                                                                        x = decuple_nested_loops(2);
                                                                                        x = 20;
                                                                                        x = x - 1;
                                                                                    }
                                                                                    x = x - 1;
                                                                                }
                                                                                x = x - 1;
                                                                            }
                                                                            x = x - 1;
                                                                        }
                                                                        x = x - 1;
                                                                    }
                                                                    x = x - 1;
                                                                }
                                                                x = x - 1;
                                                            }
                                                            x = x - 1;
                                                        }
                                                        x = x - 1;
                                                    }
                                                    x = x - 1;
                                                }
                                            x = x - 1;
                                        }
                                        x = x - 1;
                                    }
                                    x = x - 1;
                                }
                                x = x - 1;
                            }
                            x = x - 1;
                        }
                        x = x - 1;
                    }
                    x = x - 1;
                }
                x = x - 1;
            }
            x = x - 1;
        }
        x = x - 1;
    }
    return x;  
}


// int quadragintuple_nested_loops(int x)
// {
//     x = 20;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 while (x > 7)
//                                 {
//                                     while (x > 8)
//                                     {
//                                         while (x > 9)
//                                         {
//                                             while (x > 10)
//                                                 {
//                                                     while (x > 11)
//                                                     {
//                                                         while (x > 12)
//                                                         {
//                                                             while (x > 13)
//                                                             {
//                                                                 while (x > 14)
//                                                                 {
//                                                                     while (x > 15)
//                                                                     {
//                                                                         while (x > 16)
//                                                                         {
//                                                                             while (x > 17)
//                                                                             {
//                                                                                 while (x > 18)
//                                                                                 {
//                                                                                     while (x > 19)
//                                                                                     {
//                                                                                         x = vigintuple_nested_loops(2);
//                                                                                         x = 20;
//                                                                                         x = x - 1;
//                                                                                     }
//                                                                                     x = x - 1;
//                                                                                 }
//                                                                                 x = x - 1;
//                                                                             }
//                                                                             x = x - 1;
//                                                                         }
//                                                                         x = x - 1;
//                                                                     }
//                                                                     x = x - 1;
//                                                                 }
//                                                                 x = x - 1;
//                                                             }
//                                                             x = x - 1;
//                                                         }
//                                                         x = x - 1;
//                                                     }
//                                                     x = x - 1;
//                                                 }
//                                             x = x - 1;
//                                         }
//                                         x = x - 1;
//                                     }
//                                     x = x - 1;
//                                 }
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

// //THIS IS ACTUALLY SIXTY BRO: 40 + 20 = 60
// // Changed name from octogintuple_nested_loops to sexagintuple_nested_loops on
// // June 21, 2023. 09 AM
// int sexagintuple_nested_loops(int x)
// {
//     x = 20;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 while (x > 7)
//                                 {
//                                     while (x > 8)
//                                     {
//                                         while (x > 9)
//                                         {
//                                             while (x > 10)
//                                                 {
//                                                     while (x > 11)
//                                                     {
//                                                         while (x > 12)
//                                                         {
//                                                             while (x > 13)
//                                                             {
//                                                                 while (x > 14)
//                                                                 {
//                                                                     while (x > 15)
//                                                                     {
//                                                                         while (x > 16)
//                                                                         {
//                                                                             while (x > 17)
//                                                                             {
//                                                                                 while (x > 18)
//                                                                                 {
//                                                                                     while (x > 19)
//                                                                                     {
//                                                                                         x = quadragintuple_nested_loops(2);
//                                                                                         x = 20;
//                                                                                         x = x - 1;
//                                                                                     }
//                                                                                     x = x - 1;
//                                                                                 }
//                                                                                 x = x - 1;
//                                                                             }
//                                                                             x = x - 1;
//                                                                         }
//                                                                         x = x - 1;
//                                                                     }
//                                                                     x = x - 1;
//                                                                 }
//                                                                 x = x - 1;
//                                                             }
//                                                             x = x - 1;
//                                                         }
//                                                         x = x - 1;
//                                                     }
//                                                     x = x - 1;
//                                                 }
//                                             x = x - 1;
//                                         }
//                                         x = x - 1;
//                                     }
//                                     x = x - 1;
//                                 }
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

// // Changed name from actual_octogintuple_nested_loops to octogintuple_nested_loops 
// // on June 21, 2023. 09 AM
// int octogintuple_nested_loops(int x)
// {
//     x = 20;
//     while (x > 0)
//     {
//         while (x > 1)
//         {
//             while (x > 2)
//             {
//                 while (x > 3)
//                 {
//                     while (x > 4)
//                     {
//                         while (x > 5)
//                         {
//                             while (x > 6)
//                             {
//                                 while (x > 7)
//                                 {
//                                     while (x > 8)
//                                     {
//                                         while (x > 9)
//                                         {
//                                             while (x > 10)
//                                                 {
//                                                     while (x > 11)
//                                                     {
//                                                         while (x > 12)
//                                                         {
//                                                             while (x > 13)
//                                                             {
//                                                                 while (x > 14)
//                                                                 {
//                                                                     while (x > 15)
//                                                                     {
//                                                                         while (x > 16)
//                                                                         {
//                                                                             while (x > 17)
//                                                                             {
//                                                                                 while (x > 18)
//                                                                                 {
//                                                                                     while (x > 19)
//                                                                                     {
//                                                                                         x = sexagintuple_nested_loops(2);
//                                                                                         x = 20;
//                                                                                         x = x - 1;
//                                                                                     }
//                                                                                     x = x - 1;
//                                                                                 }
//                                                                                 x = x - 1;
//                                                                             }
//                                                                             x = x - 1;
//                                                                         }
//                                                                         x = x - 1;
//                                                                     }
//                                                                     x = x - 1;
//                                                                 }
//                                                                 x = x - 1;
//                                                             }
//                                                             x = x - 1;
//                                                         }
//                                                         x = x - 1;
//                                                     }
//                                                     x = x - 1;
//                                                 }
//                                             x = x - 1;
//                                         }
//                                         x = x - 1;
//                                     }
//                                     x = x - 1;
//                                 }
//                                 x = x - 1;
//                             }
//                             x = x - 1;
//                         }
//                         x = x - 1;
//                     }
//                     x = x - 1;
//                 }
//                 x = x - 1;
//             }
//             x = x - 1;
//         }
//         x = x - 1;
//     }
//     return x;  
// }

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

// int two_nested_loops(int x, int y)
// {
//     x = nested_loops(2);
//     x = nested_loops(2);
//     return x;
// }

// int three_nested_loops(int x, int y)
// {
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     return x;
// }

// int four_nested_loops(int x, int y)
// {
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     return x;
// }

// int five_nested_loops(int x, int y)
// {
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     return x;
// }

// int six_nested_loops(int x, int y)
// {
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     x = nested_loops(2);
//     return x;
// }

// TESTING triple NESTED LOOPS

// int two_triple_nested_loops(int x)
// {
//     x = triple_nested_loops(2);
//     x = triple_nested_loops(2);
//     return x;
// }

// int three_triple_nested_loops(int x)
// {
//     x = triple_nested_loops(2);
//     x = triple_nested_loops(2);
//     x = triple_nested_loops(2);
//     return x;
// }

//MIXING PRIMARY FUNCTIONS

// int first_mix(int x, int y)
// {
//     x = nested_loops(2);
// //     x = triple_nested_loops(2);
//     return x;
// }

// int two_first_mix(int x, int y)
// {
//     x = nested_loops(2);
//     x = triple_nested_loops(2);
//     x = nested_loops(2);
//     x = triple_nested_loops(2);
//     return x;
// }

// TO DO: Do a different mix
// int second_mix(int x, int y)
// {
//     x = nested_loops(2);
//     x = triple_nested_loops(2);
//     return x;
// }