#include "20_bubblesort.c"

int main() {
  int n = 10;
  long array[10] = {5, 3, 2, 1, 4, 8, 7, 9, 6, 10};

  bubble_sort(array, n);

  printf("Sorted list in ascending order:\n");

  for (int c = 0; c < n; c++) printf("%ld\n", array[c]);

  return 0;
}
