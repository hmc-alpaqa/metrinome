#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/parsing-rpn-calculator-algorithm-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "fd09419744d7494a8949a4b5f2d9a084");
	return rpn(s);
}
