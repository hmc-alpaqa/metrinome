#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/long-multiplication-1.c>
#define SIZE 10
int main() {

	const char *a;
	klee_make_symbolic(&a, sizeof(a), "6e7c61f2aa144af981f4463c452802c4");

	const char *b;
	klee_make_symbolic(&b, sizeof(b), "c97a38f1c4fc4e3581fb830e4fa66831");

	char *c;
	klee_make_symbolic(&c, sizeof(c), "2ea165b85e4747bf9f1d230a85d6dcee");
	longmulti(a, b, c);
	return 0;
}
