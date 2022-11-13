#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int *s;
	klee_make_symbolic(&s, sizeof(s), "28808e986a23448e9e0c8b1a7e68b9f3");
	return c5(s);
}
