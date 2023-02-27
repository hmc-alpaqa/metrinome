#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	node n;
	klee_make_symbolic(&n, sizeof(n), "c24d7a2494aa45da81e8441b978d2c3e");
	qinsert(n);
	return 0;
}
