#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-5.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "b99984c7cf9846bf83f646e8e24ee7c6");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int acc;
	klee_make_symbolic(&acc, sizeof(acc), "70ac38f2f8fa4140916b5b2c65dbd97a");
	if ((acc<-1) || (acc>1024)) {
		 return 0;}
	return fac_auxSafe(n, acc);
}
