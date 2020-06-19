#include "23_mergesort.c"

int main() {
  int const n = 10;
  int arr[n] = {5, 9, 1, 0, 2, 5, 11, 67, 4, 3};

  printf("Unsorted list is :\n");
  for (int i = 0; i < n; i++) printf("%d ", arr[i]);

  mergesort(arr, n);

  printf("\nSorted list is :\n");
  for (int i = 0; i < n; i++) printf("%d ", arr[i]);
  printf("\n");

  return 0;
}