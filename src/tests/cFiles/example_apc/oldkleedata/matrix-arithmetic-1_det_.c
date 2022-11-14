#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/matrix-arithmetic-1.c>
#define SIZE 10
int main() {

	double *in;
	klee_make_symbolic(&in, sizeof(in), "c6ef99e58624488dac79b2745c975e9f");

	int n;
	klee_make_symbolic(&n, sizeof(n), "67f414ab59b640ba9962740072613cbb");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int perm;
	klee_make_symbolic(&perm, sizeof(perm), "d7e5f14c20284f998ff60a4ecacff8a8");
	if ((perm<-1) || (perm>1024)) {
		 return 0;}
	return det(in, n, perm);
}
