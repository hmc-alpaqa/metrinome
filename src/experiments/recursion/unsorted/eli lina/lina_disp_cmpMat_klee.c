#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  COMPLEX** N;
  int M;
	klee_make_symbolic(&N, sizeof(N), "567f3eb64b41422d900616512f1a1a60");
  klee_make_symbolic(&M, sizeof(M), "740d219907da41a8a6aa0a06f0162fe6");
	disp_cmpMat(N, M);
  return 0;
}
