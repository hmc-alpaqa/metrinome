#include <klee/klee.h>

int get_sign(int x) {
  if (x == 0)
    return 0;

  if (x < 0)
    return -1;
  else
    return 1;
}

int main() {
  int a;
  // We need to make the variable symbolic in order to use it with klee. 
  klee_make_symbolic(&a, sizeof(a), "a");
  return get_sign(a);
}
