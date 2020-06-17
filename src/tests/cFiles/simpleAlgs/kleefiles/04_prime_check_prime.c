#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/04_prime.c>
#define SIZE 100
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "98d51e86d4d0490087688723a6a7534b");
	return check_prime(n);
}
