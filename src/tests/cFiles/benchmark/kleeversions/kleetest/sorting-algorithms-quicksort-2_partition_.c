#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-quicksort-2.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "6b807b122fce40368da948def28aaf11");

	int p;
	klee_make_symbolic(&p, sizeof(p), "29cc5112ceed4dfc8b34116225699d01");
	if ((p<-1) || (p>1024)) {
		 return 0;}

	int q;
	klee_make_symbolic(&q, sizeof(q), "8f5a30cf3c754a7b878516ec4758b478");
	if ((q<-1) || (q>1024)) {
		 return 0;}
	return partition(A, p, q);
}
