#include <stdio.h>

int checkSorted(int array[], int size);
int checkReversed(int array[], int size);

int is_sorted_or_reverse(int array[], int size) {
  int not_sorted = checkSorted(array, size);
  int not_reversed = checkReversed(array, size);

  return !not_sorted || !not_reversed;
}

int checkSorted(int array[], int size){
  int not_sorted = 0;
  for (int i = 0; i < size - 1; ++i) {
    if (array[i] > array[i + 1]) {
      not_sorted = 1;
      break;
    }
  }
  return not_sorted;
}

int checkReversed(int array[], int size){
  int not_reversed = 0;
  for (int i = 0; i < size - 1; ++i) {
    if (array[i] < array[i + 1]) {
      not_reversed = 1;
      break;
    }
  }
  return not_reversed;
}