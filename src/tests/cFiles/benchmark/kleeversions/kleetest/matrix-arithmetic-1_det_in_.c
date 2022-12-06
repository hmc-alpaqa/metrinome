#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/matrix-arithmetic-1.c>
#define SIZE 10
int main() {

	double **in;
	klee_make_symbolic(&in, sizeof(in), "ea225c1c23944575b982afb1b0f0b9c3");

	int n;
	klee_make_symbolic(&n, sizeof(n), "6fbf9fc3256543998181adaa8fade409");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int perm;
	klee_make_symbolic(&perm, sizeof(perm), "6ef271786e6e4bac896528df1012254c");
	if ((perm<-1) || (perm>1024)) {
		 return 0;}
	return det_in(in, n, perm);
}
