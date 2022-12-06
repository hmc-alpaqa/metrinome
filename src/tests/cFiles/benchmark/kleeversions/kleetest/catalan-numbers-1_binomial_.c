#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	ull m;
	klee_make_symbolic(&m, sizeof(m), "b262c1ac2382401494118602143cc6ac");

	ull n;
	klee_make_symbolic(&n, sizeof(n), "b2f3af7b01b146f0ba21200f3828a6c4");
	return binomial(m, n);
}
