#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "7b097b04be7548b7ae1f60666ee5f50d");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_iter(n);
}
