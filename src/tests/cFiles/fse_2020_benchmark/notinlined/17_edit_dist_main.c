#include "17_edit_dist.c"

// Driver program
int main() {
  int a[] = {115, 117, 110, 100, 97, 120};
  int l_a = 6;
  int b[] = {115, 97, 116, 117, 114, 100, 97, 120};
  int l_b = 8;

  int d = editDistArraysDP(a, b, l_a, l_b);
  printf("%d", d);

  return 0;
}
