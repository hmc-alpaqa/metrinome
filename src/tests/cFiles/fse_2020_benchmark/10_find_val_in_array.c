#include <stdio.h>

__attribute__((always_inline)) inline int find_first(int val, int array[], int size) {
  for (int i = 0; i < size; ++i) {
    if (array[i] == val) {
      return i;
    }
  }
  return -1;
}
