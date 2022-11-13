#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	char *p;
	klee_make_symbolic(&p, sizeof(p), "ae699af4ffe34ec4beaf07f726bfcfc5");
	reverse(p);
	return 0;
}
