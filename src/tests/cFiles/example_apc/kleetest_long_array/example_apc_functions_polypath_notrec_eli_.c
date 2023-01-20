#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "6bc2f732f8084666b19609b3e2740550");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "9fe247a79f074778aee499018f11ccd3");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return polypath_notrec_eli(n, k);
}
