#include <stdio.h>

void sign(int num) {
  if (num > 0)
      printf("%d is a positive number \n", num);
  else if (num < 0)
      printf("%d is a negative number \n", num);
  else
      printf("0 is neither positive nor negative");
}

void main()
{
  sign(5);
}
