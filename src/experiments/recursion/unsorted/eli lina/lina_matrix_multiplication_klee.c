#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int **N;
  float **M;
  float **I;
  int J;
	klee_make_symbolic(&N, sizeof(N), "53ce1833a88f4d3badbed4100e614ea3");
  klee_make_symbolic(&M, sizeof(M), "68f02b009ee84b35b268d3413dd32a60");
  klee_make_symbolic(&I, sizeof(I), "0074328b879c459a8ce15a0537ea9c4f");
  klee_make_symbolic(&J, sizeof(J), "59a4cc97190c4de4a4d955d18ccd38ca");
	matrix_multiplication(N, M, I, J);
  return 0;
}
