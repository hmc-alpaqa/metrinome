#include <stdio.h>

int main() {
  int a;
  int b;
  int c;
  int d;

  if (a > b) {
    if (b > c) {
      ++c;
    } else {
      ++b;
    }
  } else {
    ++a;
  }
  d = a + b + c;

  return 0;
}
