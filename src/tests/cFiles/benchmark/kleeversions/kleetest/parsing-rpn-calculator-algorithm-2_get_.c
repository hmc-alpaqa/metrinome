#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/parsing-rpn-calculator-algorithm-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "c8a26790f08640c8a5ac4f2475d62ec8");

	const char *e;
	klee_make_symbolic(&e, sizeof(e), "aaaeef2d284f4b328b6601edb5b35445");

	char **new_e;
	klee_make_symbolic(&new_e, sizeof(new_e), "aa6fd2b352a0485586b59510b12e8dba");
	return get(s, e, new_e);
}
