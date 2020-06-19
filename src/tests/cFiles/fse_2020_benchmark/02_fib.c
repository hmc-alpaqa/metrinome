#include <stdio.h>

int fib(int count) {
  int first_term = 0;
  int second_term = 1;
  int next_term, i;
  for (i = 1; i <= count; i++) {
    if (i <= 0)
      next_term = i;
    else {
      next_term = first_term + second_term;
      first_term = second_term;
      second_term = next_term;
    }
  }
  return next_term;
}
