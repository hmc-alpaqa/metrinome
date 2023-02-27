#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/24-game.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "bf8088bd30d34107a9907af35b5537b1");
	bail(s);
	return 0;
}
