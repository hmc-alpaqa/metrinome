#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b1;
	klee_make_symbolic(&b1, sizeof(b1), "a7655363649d4dbb9e7c25ca0fd41757");

	const char *b2;
	klee_make_symbolic(&b2, sizeof(b2), "b8fcc692ab1a4334b34ceada6d089e63");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "302af251335b4d5caca5d09953f3113b");
	mult(b1, b2, out);
	return 0;
}
