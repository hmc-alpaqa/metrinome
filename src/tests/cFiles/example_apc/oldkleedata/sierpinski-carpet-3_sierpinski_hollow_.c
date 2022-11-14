#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sierpinski-carpet-3.c>
#define SIZE 10
int main() {

	PartialGrid G;
	klee_make_symbolic(&G, sizeof(G), "26897d32fb774186ae66eeee21c0cf90");
	sierpinski_hollow(G);
	return 0;
}
