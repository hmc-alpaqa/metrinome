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

	int x;
	klee_make_symbolic(&x, sizeof(x), "e5f32f2b86624875b83e2c9d000e896d");
	return get_sign(x);
}
