#include <stdio.h>

__attribute__((always_inline)) inline  int parity(int num) {
  if (num % 2 == 0)
    return 0;
  else
    return 1;
}
