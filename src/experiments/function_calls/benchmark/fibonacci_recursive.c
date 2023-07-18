//Fibonacci Series
// copied from recursion/files/fibonacci_test.c
#include<stdio.h> 
  
int fib_rec(int n)
{
    if (n <= 1) {
        return n;
    } else {
        int a = fib_rec(n - 1);
        int b = fib_rec(n - 2);
        return a + b;
    }
}
