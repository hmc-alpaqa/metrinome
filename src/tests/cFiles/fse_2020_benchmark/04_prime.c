#include <stdio.h>
__attribute__((always_inline)) inline  int check_prime(int n) {
  int c;
  for (c = 2; c <= n - 1; c++) {
    if (n % c == 0) return 0;
  }
  return 1;
}
