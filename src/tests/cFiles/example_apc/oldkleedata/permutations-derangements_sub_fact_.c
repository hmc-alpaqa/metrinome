#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-derangements.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "c75e10efc05e4f30ae541e50b40e46a0");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return sub_fact(n);
}
