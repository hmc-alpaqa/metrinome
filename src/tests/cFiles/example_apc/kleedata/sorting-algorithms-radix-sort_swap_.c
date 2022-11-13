#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-radix-sort.c>
#define SIZE 10
int main() {

	unsigned *a;
	klee_make_symbolic(&a, sizeof(a), "5463f0e8959a4d73bc3f531119cd147e");

	unsigned *b;
	klee_make_symbolic(&b, sizeof(b), "448e7f6176f64fa5b851961ee911d88c");
	swap(a, b);
	return 0;
}
