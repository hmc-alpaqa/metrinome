#include<stdio.h>

void fib(int count){
  int first_term = 0;
  int second_term = 1;
  int next_term, i;
  printf("First %d terms of Fibonacci series:\n",count);
  for ( i = 0 ; i < count ; i++ )
  {
     if ( i <= 1 )
        next_term = i;
     else
     {
        next_term = first_term + second_term;
        first_term = second_term;
        second_term = next_term;
     }
     printf("%d\n",next_term);
  }
}
int main()
{
  fib(12);
}
