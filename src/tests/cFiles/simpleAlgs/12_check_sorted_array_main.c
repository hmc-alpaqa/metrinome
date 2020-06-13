#include "12_check_sorted_array.c"

int main() {
  const int n = 10;
  int s;
  int a[n] = {1, 2, 4, 4, 5, 7, 10, 10, 19, 23};

  s = is_sorted(a, n);
  printf("%d\n", s);
}
