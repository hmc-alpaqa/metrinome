__attribute__((always_inline)) inline int foo2(int a) {
  for (int i = 0; i < a; ++i) {
    ++a;
  }
  return a + 2;
}

__attribute__((always_inline)) inline int foo1(int a) {
  for (int i = 0; i < a; ++i) {
    foo2(a);
  }
  return a - 2;
}

int main() {
  int a;
  int b;

  b = foo1(a);

  return 0;
}
