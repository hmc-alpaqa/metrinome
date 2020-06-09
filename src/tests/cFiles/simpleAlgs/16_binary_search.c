#include <stdio.h>

int binary_search(int search, int array[], int n) {
  int first = 0;
  int last = n - 1;
  int middle = (first + last) / 2;

  while (first <= last) {
    if (array[middle] < search)
      first = middle + 1;
    else if (array[middle] > search)
      last = middle - 1;
    else if (array[middle] == search)
      return middle;
    middle = (first + last) / 2;
  }
  return -1;
}
