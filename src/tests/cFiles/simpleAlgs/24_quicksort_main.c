#include "24_quicksort.c"

int main() {
  int myArray[5] = {1, 5, 12, 0, 4};
  quickSort(&myArray[0], 5);
  printf("%d", myArray[1]);
}
