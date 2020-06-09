#include<stdio.h>

void parity(int num){
   if ( num%2 == 0 )
      printf("%d is an even number", num);
   else
      printf("%d is an odd number", num);

}

int main()
{
   // This variable is to store the input number
   int num;

   printf("Enter an integer: ");
   scanf("%d",&num);

   parity(num);

   return 0;
}
