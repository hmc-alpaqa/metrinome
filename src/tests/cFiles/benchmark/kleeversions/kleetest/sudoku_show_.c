#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sudoku.c>
#define SIZE 10
int main() {

	int *x;
	klee_make_symbolic(&x, sizeof(x), "d8b74b27ec364412852feebc7f14d23d");
	show(x);
	return 0;
}
