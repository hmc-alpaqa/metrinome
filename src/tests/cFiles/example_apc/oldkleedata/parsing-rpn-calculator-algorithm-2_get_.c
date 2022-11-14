#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/parsing-rpn-calculator-algorithm-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "5c176f2a85d04fcbb5b8bf1c79680561");

	const char *e;
	klee_make_symbolic(&e, sizeof(e), "fe2d14b99209406d955c332e1f0bd964");

	char **new_e;
	klee_make_symbolic(&new_e, sizeof(new_e), "8efd1ad478d64d04a60a01267f622dbc");
	return get(s, e, new_e);
}
