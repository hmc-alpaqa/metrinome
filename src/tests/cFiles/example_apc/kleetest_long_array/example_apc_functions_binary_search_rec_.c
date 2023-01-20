#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "035ca314e0234500a6a8ef7e354b68b1");

	int n;
	klee_make_symbolic(&n, sizeof(n), "49f7290326c346feb2492785635f41ec");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "b9adbf15ded447e19cd9a3346571640a");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_rec(A, n, x);
}
