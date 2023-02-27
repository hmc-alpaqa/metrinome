#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/multifactorial.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "fc833cf698b14a38b767691481a5ba3c");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int deg;
	klee_make_symbolic(&deg, sizeof(deg), "ba820b83762445cfbf5675df03f95678");
	if ((deg<-1) || (deg>1024)) {
		 return 0;}
	return multifact(n, deg);
}
