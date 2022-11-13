#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/multifactorial.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "f64d7b8e4fc147a5bb035fd3b1cce7b5");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int deg;
	klee_make_symbolic(&deg, sizeof(deg), "2e75d21e7a5347568a39f2bd3cf63afe");
	if ((deg<-1) || (deg>1024)) {
		 return 0;}
	return multifact_i(n, deg);
}
