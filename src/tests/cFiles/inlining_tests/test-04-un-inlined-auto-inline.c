__attribute__((always_inline)) inline int foo(int a, int b) {
  if (a > b) {
    return a - b;
  } else {
    return b - a;
  }
}

int main() {
  int a;
  int b;
  int c;

  c = foo(a, b);
  c = foo(a, b);
  c = foo(a, b);

  return 0;
}
