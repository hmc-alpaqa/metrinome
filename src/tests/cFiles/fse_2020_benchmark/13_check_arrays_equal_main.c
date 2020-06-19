#include "13_check_arrays_equal.c"

int main() {
  const int n = 10;
  int same;
  int a[n] = {1, 2, 3, 4, 5, 4, 3, 2, 1, 0};
  int b[n] = {1, 2, 3, 4, 5, 4, 3, 2, 1, 0};
  int c[n] = {1, 2, 7, 4, 5, 4, 3, 2, 1, 0};

  same = equal_arrays(a, b, n);
  printf("%d\n", same);

  same = equal_arrays(a, c, n);
  printf("%d\n", same);
}
