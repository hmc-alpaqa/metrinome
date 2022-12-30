#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "16ede72f010946a6825b7903069307c2");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "4fa5addd73a444ae9c9246f81619110f");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_rec(x, n);
}
