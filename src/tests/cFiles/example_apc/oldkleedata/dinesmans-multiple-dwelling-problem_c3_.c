#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/dinesmans-multiple-dwelling-problem.c>
#define SIZE 10
int main() {

	int *s;
	klee_make_symbolic(&s, sizeof(s), "4acbe9f5a1e84a99a2af3101ca3ac5f7");
	return c3(s);
}
