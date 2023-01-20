#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "736950372cec427c8e591db1e8292969");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "09fb1138edbb4c139efdc2b7490bfb80");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return polypath_rec_eli(n, k);
}
