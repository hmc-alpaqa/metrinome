#include <stdio.h>
__attribute__((always_inline)) inline int insertion_sort(int list[], int count) {
  int i, j, temp;
  for (i = 1; i < count; i++) {
    temp = list[i];
    j = i - 1;
    while (temp < list[j] && j >= 0) {
      list[j + 1] = list[j];
      j = j - 1;
    }
    list[j + 1] = temp;
  }

  return 0;
}
