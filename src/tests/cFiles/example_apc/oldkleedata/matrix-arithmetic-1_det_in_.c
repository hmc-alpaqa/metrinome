#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/matrix-arithmetic-1.c>
#define SIZE 10
int main() {

	double **in;
	klee_make_symbolic(&in, sizeof(in), "afc4e4783eb242d19926388588b039c2");

	int n;
	klee_make_symbolic(&n, sizeof(n), "f652b4b38cd84cffb74fb313c379e843");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int perm;
	klee_make_symbolic(&perm, sizeof(perm), "d8100974c59f442cb1150f7b9b9e61e5");
	if ((perm<-1) || (perm>1024)) {
		 return 0;}
	return det_in(in, n, perm);
}
