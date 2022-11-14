#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sudoku.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "d99ca73447b7435c831ce96a87380ec8");
	solve(s);
	return 0;
}
