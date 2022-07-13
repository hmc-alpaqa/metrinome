/* Include statements and constant definitions */
#include <stdio.h>
#define HIGHEST_DEGREE 5
#define LARGEST_NUMBER 10

/* Recursive implementation of multifactorial function */
int multifact(int n, int deg){
   return n <= deg ? n : n * multifact(n - deg, deg);
}

/* Iterative implementation of multifactorial function */
int multifact_i(int n, int deg){
   int result = n;
   while (n >= deg + 1){
      result *= (n - deg);
      n -= deg;
   }
   return result;
}

/* Test function to print out multifactorials */
