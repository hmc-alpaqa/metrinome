#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/multifactorial.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "28c1f7c939224021acd2a8524023f376");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int deg;
	klee_make_symbolic(&deg, sizeof(deg), "e51cb4e900fb40dc92a89571357e53ce");
	if ((deg<-1) || (deg>1024)) {
		 return 0;}
	return multifact(n, deg);
}
