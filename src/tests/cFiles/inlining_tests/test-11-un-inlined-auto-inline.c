__attribute__((always_inline)) inline int foo(int a, int b) {
  for (int i = 0; i < a; ++i) {
    ++a;
  }
  for (int i = 0; i < b; ++i) {
    ++b;
  }
  return a * b;
}

int main() {
  int a;
  int b;
  int c;

  c = foo(a, b);

  return 0;
}
