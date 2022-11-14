#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/stern-brocot-sequence-1.c>
#define SIZE 10
int main() {

	uint n;
	klee_make_symbolic(&n, sizeof(n), "14c7e9bdd2d44a7bbea336796dac7cad");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return f(n);
}
