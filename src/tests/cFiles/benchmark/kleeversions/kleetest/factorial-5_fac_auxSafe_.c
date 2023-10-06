#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-5.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "613bb01a92944f6f91c51a7c7c61b182");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int acc;
	klee_make_symbolic(&acc, sizeof(acc), "247389696188448097a00a48e110525b");
	if ((acc<-1) || (acc>1024)) {
		 return 0;}
	return fac_auxSafe(n, acc);
}
