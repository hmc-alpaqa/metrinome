#include <stdio.h>

__attribute__((always_inline)) inline void selection_sort(int list[], int count) {
  int i, j, temp;
  for (i = 0; i < count; i++) {
    for (j = i + 1; j < count; j++) {
      if (list[i] > list[j]) {
        temp = list[i];
        list[i] = list[j];
        list[j] = temp;
      }
    }
  }
}
