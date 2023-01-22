#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "19e17be313e24a1f8a9357b4d94e36d3");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "1eee2429d2f544e5bd928312d52e5110");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return polypath_notrec_eli(n, k);
}
