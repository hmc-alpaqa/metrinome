#include "50_check_sorted_or_reverse_wHelper.c"

int main() {
  const int n = 10;
  int s;
  int a[n] = {1, 2, 4, 4, 5, 7, 10, 10, 19, 23};

  s = is_sorted_or_reverse(a, n);
  printf("%d\n", s);


  int b[n] = {1, 2, 4, 4, 5, 11, 10, 10, 19, 23};

  s = is_sorted_or_reverse(b, n);
  printf("%d\n", s);

  int c[n] = {100, 90, 80, 70, 60, 50, 40, 30, 20, 10};

  s = is_sorted_or_reverse(c, n);
  printf("%d\n", s);


}
