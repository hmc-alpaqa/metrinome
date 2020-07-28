#include <stdio.h>

int main() {
  int a;
  int b;
  int c;
  int d;

  if (b > a) {
    c = b;
  } else {
    if (a < 0) {
      c = a + 10;
    } else {
      c = a;
    }
  }

  if (a < 0) {
    d = a + 10;
  }

  return 0;
}
