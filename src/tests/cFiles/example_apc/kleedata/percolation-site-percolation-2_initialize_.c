#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/percolation-site-percolation-2.c>
#define SIZE 10
int main() {

	Grid grid;
	klee_make_symbolic(&grid, sizeof(grid), "7be647f2c5524b8cac38108d4b9db88e");

	const double probability;
	klee_make_symbolic(&probability, sizeof(probability), "582b7e2a8f134df89c98b836c1bd7b48");
	initialize(grid, probability);
	return 0;
}
