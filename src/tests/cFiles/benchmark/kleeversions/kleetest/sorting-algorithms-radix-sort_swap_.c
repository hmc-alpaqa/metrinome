#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-radix-sort.c>
#define SIZE 10
int main() {

	unsigned *a;
	klee_make_symbolic(&a, sizeof(a), "d39e5983e161420c99d7962663c03694");

	unsigned *b;
	klee_make_symbolic(&b, sizeof(b), "58ee4df1279548bfb564002d59e58e71");
	swap(a, b);
	return 0;
}
