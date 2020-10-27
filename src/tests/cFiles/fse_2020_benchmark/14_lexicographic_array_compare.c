#include <stdio.h>

__attribute__((always_inline)) inline int compare_arrays(int x[], int y[], int size) {
  for (int i = 0; i < size; ++i) {
    if (x[i] < y[i]) {
      return -1;
    } else if (x[i] > y[i]) {
      return 1;
    }
  }
  return 0;
}
