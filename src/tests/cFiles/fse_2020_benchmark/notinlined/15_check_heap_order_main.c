#include "15_check_heap_order.c"

int main() {
  const int n = 10;
  int a[10] = {4, 10, 7, 41, 52, 10, 13, 43, 45, 60};
  int h = is_heap_order(a, n);
  printf("%d\n", h);
  return 0;
}
