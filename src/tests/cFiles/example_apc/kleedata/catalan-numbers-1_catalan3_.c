#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/catalan-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "c10284f22e844472a9d1afc5680f2a3d");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return catalan3(n);
}
