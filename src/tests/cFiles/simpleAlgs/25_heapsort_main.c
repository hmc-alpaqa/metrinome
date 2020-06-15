#include "25_heapsort.c"

void display(int a[], const int size) {
  int i;
  for (i = 0; i < size; i++) printf("%d ", a[i]);

  printf("\n");
}

int main() {

  const int n = 10;
  int a[n] = {8, 5, 2, 3, 1, 6, 9, 4, 0, 7};

  printf("Array before sorting:\n");
  display(a, n);

  heap_sort(a, n);

  printf("Array after sorting:\n");
  display(a, n);

  return 0;
}
