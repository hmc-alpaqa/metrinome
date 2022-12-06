#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b1;
	klee_make_symbolic(&b1, sizeof(b1), "570e2c5fc07a477db5c4f3309196677f");

	const char *b2;
	klee_make_symbolic(&b2, sizeof(b2), "c2c93058f4a34c22946abcd542d4f348");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "896c359431d34633ad8aa6c1681d45be");
	mult(b1, b2, out);
	return 0;
}
