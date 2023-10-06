#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "150a4abbfd244407b3b8974b80ab8d4e");
	show(grid);
	return 0;
}
