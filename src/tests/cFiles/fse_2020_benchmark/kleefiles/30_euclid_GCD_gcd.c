#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/30_euclid_GCD.c>
#define SIZE 100
int main() {

	int a;
	klee_make_symbolic(&a, sizeof(a), "0df5981a3a334599a28fc6ecc7b60437");

	int b;
	klee_make_symbolic(&b, sizeof(b), "c036fb0ff3bf410b8f07539e732e276c");
	return gcd(a, b);
}
