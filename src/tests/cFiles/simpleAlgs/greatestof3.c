#include<stdio.h>


void greatestof3(int num1, int num2, int num3){

  if((num1>num2)&&(num1>num3))
     printf("\n Number1 is greatest");
  else if((num2>num3)&&(num2>num1))
     printf("\n Number2 is greatest");
  else
     printf("\n Number3 is greatest");
}
int main()
{
  greatestof3(5,12,2);
}
