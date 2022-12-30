#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "b7a907c750dc4dcaa39942f645f0bc85");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "1ddfe5624d034ab2804d01d946884e16");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return polypath_notrec_eli(n, k);
}
