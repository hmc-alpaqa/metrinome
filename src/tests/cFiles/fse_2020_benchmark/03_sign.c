#include <stdio.h>

__attribute__((always_inline)) inline  int sign(int num) {
  if (num > 0)
    return 1;
  else if (num < 0)
    return -1;
  else
    return 0;
}
