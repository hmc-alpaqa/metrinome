#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	node *el;
	klee_make_symbolic(&el, sizeof(el), "1d2fd646d3e0457aaee1a4aa6af77e46");
	cleanHelp(el);
	return 0;
}
