#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/arbitrary-precision-integers--included--3.c>
#define SIZE 10
int main() {

	const unsigned char *N;
  const unsigned char *M;
	klee_make_symbolic(&N, sizeof(N), "9f25a68b94aa46208fe8c3f05d3053d2");
  klee_make_symbolic(&M, sizeof(M), "690c7ce70dbb4fcab1b0fe29d605124f");
	str_mult(N, M);
  return 0;
}
