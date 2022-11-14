#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	ull m;
	klee_make_symbolic(&m, sizeof(m), "3ad77aed20fd4814b7775c22b2013ca4");

	ull n;
	klee_make_symbolic(&n, sizeof(n), "1f3be9b1427948959e439dc5a0b68728");
	return binomial(m, n);
}
