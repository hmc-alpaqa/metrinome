#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  double** N;
  double** M;
  int* I;
  double* J;
  int K;
	klee_make_symbolic(&N, sizeof(N), "53ce1833a88f4d3badbed4100e614ea3");
  klee_make_symbolic(&M, sizeof(M), "68f02b009ee84b35b268d3413dd32a60");
  klee_make_symbolic(&I, sizeof(I), "0074328b879c459a8ce15a0537ea9c4f");
  klee_make_symbolic(&J, sizeof(J), "951fc7dc278547aa96faea580f2a9c00");
  klee_make_symbolic(&K, sizeof(K), "b71965996bae4cd494d9d4b6cbd5ea1c");
	lup_sol(N, M, I, J, K);
  return 0;
}
