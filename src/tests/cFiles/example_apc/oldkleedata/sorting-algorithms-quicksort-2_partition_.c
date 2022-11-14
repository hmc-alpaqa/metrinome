#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-2.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "41afc2d611df47008049bd4c31554c98");

	int p;
	klee_make_symbolic(&p, sizeof(p), "4e8724c04cd14b26aa3d7b55a835a3b5");
	if ((p<-1) || (p>1024)) {
		 return 0;}

	int q;
	klee_make_symbolic(&q, sizeof(q), "fdf415fdfd7548f18a52518840a1dff2");
	if ((q<-1) || (q>1024)) {
		 return 0;}
	return partition(A, p, q);
}
