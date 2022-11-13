#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-5.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "30235cee4428476f9b43a58eb58f26e2");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int acc;
	klee_make_symbolic(&acc, sizeof(acc), "022d95df51044f97a155e9d87942418d");
	if ((acc<-1) || (acc>1024)) {
		 return 0;}
	return fac_aux(n, acc);
}
