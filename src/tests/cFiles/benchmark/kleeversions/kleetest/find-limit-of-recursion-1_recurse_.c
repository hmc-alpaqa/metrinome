#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/find-limit-of-recursion-1.c>
#define SIZE 10
int main() {

	unsigned int i;
	klee_make_symbolic(&i, sizeof(i), "6d41fc7899bf452380e8aebcb8ae067b");
	if ((i<-1) || (i>1024)) {
		 return 0;}
	recurse(i);
	return 0;
}
