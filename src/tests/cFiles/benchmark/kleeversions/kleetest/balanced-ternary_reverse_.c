#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	char *p;
	klee_make_symbolic(&p, sizeof(p), "c80ffc4cc9294edd867d45e1bc24cf89");
	reverse(p);
	return 0;
}