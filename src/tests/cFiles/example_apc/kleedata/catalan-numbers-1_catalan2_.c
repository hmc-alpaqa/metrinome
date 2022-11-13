#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "01120108a87347fd8f870e87efd738b6");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return catalan2(n);
}
