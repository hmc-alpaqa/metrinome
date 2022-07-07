#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  Vector* N;
  Vector* M;
  Vector* I;
  Vector* J;
	klee_make_symbolic(&N, sizeof(N), "53ce1833a88f4d3badbed4100e614ea3");
  klee_make_symbolic(&M, sizeof(M), "68f02b009ee84b35b268d3413dd32a60");
  klee_make_symbolic(&I, sizeof(I), "d158bef87c2f467aab6444b3e6103705");
  klee_make_symbolic(&J, sizeof(J), "8ddf252d9cf44210b0676ce3dd31747e");
	vectorTripleProduct(N, M, I, J);
  return 0;
}
