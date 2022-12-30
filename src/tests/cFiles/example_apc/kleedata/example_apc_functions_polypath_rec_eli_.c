#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "e63cf9ff2452465bbe55fff0c6b15c83");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "988b4e3cedd947f8b4ba30eff55b7437");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return polypath_rec_eli(n, k);
}
