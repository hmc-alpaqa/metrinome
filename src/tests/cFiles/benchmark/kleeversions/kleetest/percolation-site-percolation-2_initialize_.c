#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "ed6ae2aaca9f416d9d5e2e082be76679");

	const double probability;
	klee_make_symbolic(&probability, sizeof(probability), "475fe0d65fa04db3af4c89745d7e2825");
	initialize(grid, probability);
	return 0;
}
