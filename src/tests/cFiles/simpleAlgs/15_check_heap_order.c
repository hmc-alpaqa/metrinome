#include <stdio.h>

int is_heap_order(int a[], int n) {
  for (int i = 0; i < (n - 2) / 2; ++i) {
    if (a[i] >= a[2 * i + 1] || a[i] >= a[2 * i + 2]) {
      return 0;
    }
  }
  return 1;
}
