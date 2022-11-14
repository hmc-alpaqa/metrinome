#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-2.c>
#define SIZE 10
int main() {

	int *a;
	klee_make_symbolic(&a, sizeof(a), "2f78b5c66bb54494b504f22059881016");

	int *b;
	klee_make_symbolic(&b, sizeof(b), "b52322d8f3404a31a8ae9977c5089988");
	swap(a, b);
	return 0;
}
