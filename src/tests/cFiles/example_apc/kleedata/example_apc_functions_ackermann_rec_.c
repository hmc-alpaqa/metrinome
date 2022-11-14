#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "f4ecc8d2a9ea48d2b7aa7f75aeaa9d91");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "f6b7627a3b7b41fab3ae2d034842cd3f");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return ackermann_rec(m, n);
}
