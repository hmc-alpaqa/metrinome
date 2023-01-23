#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "a0e9b6fb2d384241bf7f6e6e33b07927");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int k;
	klee_make_symbolic(&k, sizeof(k), "c84d88fbcb374ff2a1f6eacb703039e4");
	if ((k<-1) || (k>1024)) {
		 return 0;}
	return polypath_rec_eli(n, k);
}
