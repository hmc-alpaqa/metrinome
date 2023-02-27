#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-2.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "0b689b5835be4849b72339db19869d90");

	int p;
	klee_make_symbolic(&p, sizeof(p), "2d1dda148440477e91b5f00d55d0b4c5");
	if ((p<-1) || (p>1024)) {
		 return 0;}

	int q;
	klee_make_symbolic(&q, sizeof(q), "ec6a01ee65194425b0e398bb6c967b4f");
	if ((q<-1) || (q>1024)) {
		 return 0;}
	quicksort(A, p, q);
	return 0;
}
