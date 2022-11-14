#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int *s;
	klee_make_symbolic(&s, sizeof(s), "32f501f06b414838951875107dc116a0");
	return c1(s);
}
