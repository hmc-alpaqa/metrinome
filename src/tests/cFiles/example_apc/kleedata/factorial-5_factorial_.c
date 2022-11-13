#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-5.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "77b75cf4bcfc4c9b8c110fcd29f511bf");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorial(n);
}
