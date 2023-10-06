#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "754c85ed0d7b42af8204e25c701639c0");
	return percolate(grid);
}
