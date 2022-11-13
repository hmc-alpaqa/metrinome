#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "f068bfb569bb4f629ae578a894683d4e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return catalan1(n);
}
