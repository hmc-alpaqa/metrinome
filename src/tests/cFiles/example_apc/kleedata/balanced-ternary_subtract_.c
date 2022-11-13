#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b1;
	klee_make_symbolic(&b1, sizeof(b1), "cb218a3320c2415da922396e12ac44b6");

	const char *b2;
	klee_make_symbolic(&b2, sizeof(b2), "c4cd9daefe444a61914af956a3b013bc");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "048110935e2c4d248b5d7e5d8468dbc6");
	subtract(b1, b2, out);
	return 0;
}
