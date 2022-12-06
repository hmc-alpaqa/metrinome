#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/permutations-derangements.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "4748f327edfd46c39e68a2341dcd16b5");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return sub_fact(n);
}
