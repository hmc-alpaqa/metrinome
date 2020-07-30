__attribute__((always_inline)) inline int foo1(int a, int b) {
  for (int i = 0; a < i; ++i) {
    if (a < b) {
      ++a;
    } else {
      ++b;
    }
  }
  return a;
}

int main() {
  int a;
  int b;
  int c;

  c = foo1(a, b);

  return 0;
}
