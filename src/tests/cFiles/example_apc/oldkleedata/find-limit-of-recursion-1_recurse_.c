#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/find-limit-of-recursion-1.c>
#define SIZE 10
int main() {

	unsigned int i;
	klee_make_symbolic(&i, sizeof(i), "8f42e2e18b51413eb954dda331cc4e42");
	if ((i<-1) || (i>1024)) {
		 return 0;}
	recurse(i);
	return 0;
}
