#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sudoku.c>
#define SIZE 10
int main() {

	int *x;
	klee_make_symbolic(&x, sizeof(x), "bc1b029bea804ecd9e0506a181fa900a");
	show(x);
	return 0;
}
