#include <stdio.h>

int equal_arrays(int x[], int y[], int size) {
  for (int i = 0; i < size; ++i) {
    if (x[i] != y[i]) {
      return 0;
    }
  }
  return 1;
}
