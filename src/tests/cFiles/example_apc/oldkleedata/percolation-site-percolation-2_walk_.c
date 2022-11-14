#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "2471a6dee09743639121a908a62f5091");

	const size_t r;
	klee_make_symbolic(&r, sizeof(r), "c4d361a9667143b296a3139d93dc028d");

	const size_t c;
	klee_make_symbolic(&c, sizeof(c), "29a344fff6c048eca515626f40c370ef");
	return walk(grid, r, c);
}
