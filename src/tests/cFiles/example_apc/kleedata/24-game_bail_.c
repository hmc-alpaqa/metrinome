#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/24-game.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "313ad819bdd841d3b363b12030645c56");
	bail(s);
	return 0;
}
