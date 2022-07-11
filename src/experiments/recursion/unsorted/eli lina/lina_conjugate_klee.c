#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  struct complex_no N;
	klee_make_symbolic(&N, sizeof(N), "abc1f4ea588d453294d8b5f691acbc19");
	conjugate(N);
  return 0;
}
