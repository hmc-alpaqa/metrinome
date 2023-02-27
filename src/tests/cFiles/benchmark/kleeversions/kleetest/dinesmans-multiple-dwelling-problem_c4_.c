#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int *s;
	klee_make_symbolic(&s, sizeof(s), "0c1520e99e4440e39fe957adda8c24a8");
	return c4(s);
}
