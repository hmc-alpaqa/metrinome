#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int *s;
	klee_make_symbolic(&s, sizeof(s), "3e92f3ad4e7a4df29b6b58f9e561a9f6");
	return c3(s);
}
