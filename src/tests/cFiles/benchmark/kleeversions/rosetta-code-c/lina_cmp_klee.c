#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int N;
  int M;
	klee_make_symbolic(&N, sizeof(N), "6eefcea6c7044fd4b13c86650f51748d");
  klee_make_symbolic(&M, sizeof(M), "5ca3b4a1c63a4931adff70a657190bd4");

	cmp(N, M);
  return 0;
}
