#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "17df9195c87f489fb2ff9e8307d0fb31");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorial(n);
}
