int foo2(int a) {
  if (a < 0) {
    return a + 10;
  } else {
    return a;
  }
}

int foo1(int a, int b) {
  if (b > a) {
    return b;
  } else {
    return foo2(b);
  }
}

int main() {
  int a;
  int b;
  int c;
  int d;

  c = foo1(a, b);
  d = foo2(b);

  return 0;
}
