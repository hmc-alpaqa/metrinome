#include<stdio.h>

int parity(int num){
   if ( num % 2 == 0 )
      return 0   ;
   else
      return 1;
}

int main()
{
   // This variable is to store the input number
   int num = 9;
   int p = parity(num);
   printf("%d\n", p);
   return 0;
}
