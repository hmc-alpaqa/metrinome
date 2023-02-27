#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/mutual-recursion.c>
#define SIZE 10
int main() {

	const int n;
	klee_make_symbolic(&n, sizeof(n), "90bfa96265cb4918aff367623fee1ae4");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return M(n);
}
