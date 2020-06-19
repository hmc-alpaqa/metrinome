#include "19_longest_common_increasing_subsequence.c"

int main() {
  int arr1[] = {3, 4, 9, 1};
  int arr2[] = {5, 3, 8, 9, 10, 2, 1};

  int n = sizeof(arr1) / sizeof(arr1[0]);
  int m = sizeof(arr2) / sizeof(arr2[0]);

  printf("Length of LCIS is %d\n", LCIS(arr1, n, arr2, m));
  return (0);
}
