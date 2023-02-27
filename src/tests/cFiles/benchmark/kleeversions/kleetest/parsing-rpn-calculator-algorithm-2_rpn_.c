#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/parsing-rpn-calculator-algorithm-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "473da2b654be4ea6971bd6cae4d08d51");
	return rpn(s);
}
