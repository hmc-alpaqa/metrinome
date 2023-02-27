#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	PartialGrid G;
	klee_make_symbolic(&G, sizeof(G), "580a0563363c4e2ab7f43f9e6487f750");
	sierpinski_hollow(G);
	return 0;
}
