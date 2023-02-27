#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "f93f5ac4f8e34b78ab6926c73d61108e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return catalan3(n);
}
