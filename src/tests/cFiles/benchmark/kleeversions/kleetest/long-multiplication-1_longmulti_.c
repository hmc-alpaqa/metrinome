#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/long-multiplication-1.c>
#define SIZE 10
int main() {

	const char *a;
	klee_make_symbolic(&a, sizeof(a), "5a0f35e386a64877b679c929a7bd4d9b");

	const char *b;
	klee_make_symbolic(&b, sizeof(b), "33bafd80897c4dc9aaaf6119284f5e6b");

	char *c;
	klee_make_symbolic(&c, sizeof(c), "1ae363d7a1bc4a1192baf69fdebe9f7e");
	longmulti(a, b, c);
	return 0;
}
