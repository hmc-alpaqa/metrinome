#include <stdio.h>

__attribute__((always_inline)) inline int is_sorted_or_reverse(int array[], int size) {
  int not_sorted = 0;
  for (int i = 0; i < size - 1; ++i) {
    if (array[i] > array[i + 1]) {
      not_sorted = 1;
      break;
    }
  }

  int not_reversed = 0;
  for (int i = 0; i < size - 1; ++i) {
    if (array[i] < array[i + 1]) {
      not_reversed = 1;
      break;
    }
  }

  return !not_sorted || !not_reversed;
}
