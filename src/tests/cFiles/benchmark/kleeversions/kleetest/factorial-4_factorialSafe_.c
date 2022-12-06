#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-4.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "c6098526a62a43bebb13f346ef291157");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorialSafe(n);
}
