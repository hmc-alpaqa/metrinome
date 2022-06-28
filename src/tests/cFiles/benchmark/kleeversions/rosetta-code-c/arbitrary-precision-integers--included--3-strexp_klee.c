#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/arbitrary-precision-integers--included--3.c>
#define SIZE 10
int main() {

	int N;
  int M;
	klee_make_symbolic(&N, sizeof(N), "9a09f0c5f3f341eea906fd2266c11994");
  klee_make_symbolic(&M, sizeof(M), "faf34da01808437987ca30a7f41536b1");
	str_exp(N, M);
  return 0;
}
