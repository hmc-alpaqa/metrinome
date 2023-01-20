#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "6ffc10be8ac14237aa49d8bd3cf0b7dc");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "804e48abf3af45d28b6ac6376a07e1aa");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return ackermann_rec(m, n);
}
