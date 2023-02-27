#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b1;
	klee_make_symbolic(&b1, sizeof(b1), "a4528cd949664ca28ee19f542956d82c");

	const char *b2;
	klee_make_symbolic(&b2, sizeof(b2), "f554b2c5d0024e80b189768f2eb2d292");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "fe3ff1216ac246779f2f8bf574cf003a");
	add(b1, b2, out);
	return 0;
}
