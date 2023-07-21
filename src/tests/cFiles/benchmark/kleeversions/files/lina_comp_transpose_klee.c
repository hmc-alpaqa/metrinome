#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  COMPLEX ** N;
  int M;
	klee_make_symbolic(&N, sizeof(N), "1fc09079426949b28901582082578330");
  klee_make_symbolic(&M, sizeof(M), "bceee848e5584cc9a58654ccd7cd5163");
	comp_transpose(N, M);
  return 0;
}
