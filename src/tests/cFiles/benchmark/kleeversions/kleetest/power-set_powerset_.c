#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/power-set.c>
#define SIZE 10
int main() {

	char **v;
	klee_make_symbolic(&v, sizeof(v), "d444987e41bb491ba50c9a543306e937");

	int n;
	klee_make_symbolic(&n, sizeof(n), "68078ebe30cf4a83bfd392ed92db5dc3");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	struct node *up;
	klee_make_symbolic(&up, sizeof(up), "b220eb7fcf004113aa5d47776424335c");
	powerset(v, n, up);
	return 0;
}
