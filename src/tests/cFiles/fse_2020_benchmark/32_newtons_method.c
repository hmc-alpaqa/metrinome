// https://www.codewithc.com/c-program-for-newton-raphson-method/

#include <stdio.h>
__attribute__((always_inline)) inline float f(float x) { return 3 * x * x + 2 * x - 15.7; }

__attribute__((always_inline)) inline float df(float x) { return 6 * x + 2; }

__attribute__((always_inline)) inline float newton_root(float x0, float allerr, int maxmitr) {
  float h, abs_h, x1;
  for (int itr = 1; itr <= maxmitr; itr++) {
    h = f(x0) / df(x0);
    x1 = x0 - h;
    printf(" At Iteration no. %3d, x = %9.6f\n", itr, x1);
    abs_h = (h > 0) ? h : -h;
    if (abs_h < allerr) {
      printf("After %3d iterations, root = %8.6f\n", itr, x1);
      return x1;
    }
    x0 = x1;
  }
  printf(
      " The required solution does not converge or iterations are "
      "insufficient\n");
  return x1;
}
