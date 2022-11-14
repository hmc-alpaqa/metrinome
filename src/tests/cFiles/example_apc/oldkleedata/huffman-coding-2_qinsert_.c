#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	node n;
	klee_make_symbolic(&n, sizeof(n), "9df9b775ee024a9d9b0180f6ca3e5357");
	qinsert(n);
	return 0;
}
