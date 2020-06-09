#include <stdio.h>

int sign(int num) {
  if (num > 0)
    return 1;
  else if (num < 0)
      return -1;
  else
      return 0;
}

int main()
{
  int s = sign(-5);
  printf("%d", s);
}
