int __attribute__((always_inline)) inline static foo(int a, int b, int c) {
  if (a > b) {
    if (b > c) {
      ++c;
    } else {
      ++b;
    }
  } else {
    ++a;
  }
  return a + b + c;
}

int main() {
  int a;
  int b;
  int c;
  int d;

  d = foo(a, b, c);

  return 0;
}
