#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-5.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "1dffadafb6a64d288f3bfd03062b4f4d");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int acc;
	klee_make_symbolic(&acc, sizeof(acc), "e9c9acd498a84bacaa056ad2d1aac2c7");
	if ((acc<-1) || (acc>1024)) {
		 return 0;}
	return fac_aux(n, acc);
}
