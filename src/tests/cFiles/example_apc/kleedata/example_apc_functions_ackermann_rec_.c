#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int m;
	klee_make_symbolic(&m, sizeof(m), "c1b4f63acd0c40a286c5d241d1ec2dde");
	if ((m<-1) || (m>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "2f579120774d4381aa9a5cc58365e08b");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return ackermann_rec(m, n);
}
