int foo(int a, int b, int c) {
  for (int i = 0; i < a; ++i) {
    for (int j = 0; j < b; ++j) {
      ++c;
    }
  }
  return a + b;
}

int main() {
  int a;
  int b;
  int c;
  int d;

  d = foo(a, b, c);

  return 0;
}
