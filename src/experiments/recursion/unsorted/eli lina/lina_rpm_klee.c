#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  double** N;
	klee_make_symbolic(&N, sizeof(N), "2506278163d64731af0da76415cd6b24");
	rpm(N);
  return 0;
}
