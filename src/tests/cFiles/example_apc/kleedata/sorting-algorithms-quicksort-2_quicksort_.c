#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-2.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "c2e122bee3a044a2b4356b3a73896945");

	int p;
	klee_make_symbolic(&p, sizeof(p), "3089953fdee344b680bd7f8ba4e4a40c");
	if ((p<-1) || (p>1024)) {
		 return 0;}

	int q;
	klee_make_symbolic(&q, sizeof(q), "12badfa0cfa44af5ac4323baa7ef33aa");
	if ((q<-1) || (q>1024)) {
		 return 0;}
	quicksort(A, p, q);
	return 0;
}
