#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "408a80516c2343328cc165052187b2d7");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorial(n);
}
