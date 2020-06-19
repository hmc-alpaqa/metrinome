#include "16_binary_search.c"

int main() {
  const int n = 10;  // number of elements
  int val = 13;
  int array[10] = {2, 4, 8, 10, 12, 15, 19, 20, 22, 30};

  int location = binary_search(val, array, n);

  printf("%d\n", location);
  return 0;
}
