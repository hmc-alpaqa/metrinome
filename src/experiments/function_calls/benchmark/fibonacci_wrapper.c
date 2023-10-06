
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

int fib_rec_wrapper(int n){
    return fib_rec(n);
}