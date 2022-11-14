#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "2ffaa07d4d6749ba9eb4d4675c16e9b3");
	show(grid);
	return 0;
}
