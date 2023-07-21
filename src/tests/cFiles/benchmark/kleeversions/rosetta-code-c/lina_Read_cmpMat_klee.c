#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  COMPLEX **N;
  int M;
	klee_make_symbolic(&N, sizeof(N), "53ce1833a88f4d3badbed4100e614ea3");
  klee_make_symbolic(&M, sizeof(M), "68f02b009ee84b35b268d3413dd32a60");
	Read_cmpMat(N, M);
  return 0;
}
