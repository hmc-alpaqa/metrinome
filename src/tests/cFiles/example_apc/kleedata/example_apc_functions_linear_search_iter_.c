#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "eb15b3f7a8dc45b490193ecd70248ea1");

	int n;
	klee_make_symbolic(&n, sizeof(n), "a4167b982c8842bba91733a3a0b7a011");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "f641ecce334143e3a648032f4d0543d6");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_iter(A, n, x);
}
