#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-2.c>
#define SIZE 10
int main() {

	int *a;
	klee_make_symbolic(&a, sizeof(a), "c9020a0d44964bd8afc632d3a0fd9e35");

	int *b;
	klee_make_symbolic(&b, sizeof(b), "ec463f5de4f7488282bf39f6a8312b94");
	swap(a, b);
	return 0;
}
