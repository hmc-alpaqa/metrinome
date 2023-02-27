#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "758345ded8fb42dabf21861a6f148f6c");

	const size_t r;
	klee_make_symbolic(&r, sizeof(r), "e7eb083b9dac4679a45da6b7cec26fc2");

	const size_t c;
	klee_make_symbolic(&c, sizeof(c), "c94f3b86619c48a9b2dea0d1f8ff5137");
	return walk(grid, r, c);
}
