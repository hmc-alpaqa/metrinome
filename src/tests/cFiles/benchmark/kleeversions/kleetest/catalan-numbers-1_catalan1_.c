#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "94781b7fcaf7480e84f7dcf4451d84df");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return catalan1(n);
}
