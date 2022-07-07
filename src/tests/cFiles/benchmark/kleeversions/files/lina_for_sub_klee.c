#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int* N;
  double* M;
  double** I;
  int J;
	klee_make_symbolic(&N, sizeof(N), "53ce1833a88f4d3badbed4100e614ea3");
  klee_make_symbolic(&M, sizeof(M), "68f02b009ee84b35b268d3413dd32a60");
  klee_make_symbolic(&I, sizeof(I), "2706dd4014c14f59915ba6c3fcc2e468");
  klee_make_symbolic(&J, sizeof(J), "1fc60062f97c4dfab843ed1d42473f5b");
	for_sub(N, M, I, J);
  return 0;
}
