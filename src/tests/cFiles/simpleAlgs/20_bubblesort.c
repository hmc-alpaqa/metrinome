#include <stdio.h>

void bubble_sort(long list[], long n)
{
  long c, d, t;

  for (c = 0 ; c < n - 1; c++) {
    for (d = 0 ; d < n - c - 1; d++) {
      if (list[d] > list[d+1]) {
        /* Swapping */
        t         = list[d];
        list[d]   = list[d+1];
        list[d+1] = t;
      }
    }
  }
}

int main() {
  int n = 10;
  long array[10] = {5,3,2,1,4,8,7,9,6,10};

  bubble_sort(array, n);

  printf("Sorted list in ascending order:\n");

  for (int c = 0; c < n; c++)
     printf("%ld\n", array[c]);

  return 0;
}
