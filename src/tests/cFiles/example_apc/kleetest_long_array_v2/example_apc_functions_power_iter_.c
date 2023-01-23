#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "94961b32001f4038a7e239a736802bfa");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "b82c4ed382d74e50a3cf72f724071790");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_iter(x, n);
}
