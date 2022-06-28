#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/arena-storage-pool-7.c>
#define SIZE 10
int main() {

	size_t N;
	klee_make_symbolic(&N, sizeof(N), "9f25a68b94aa46208fe8c3f05d3053d2");
	customFree(N);
  return 0;
}
