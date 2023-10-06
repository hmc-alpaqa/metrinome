#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/matrix-arithmetic-1.c>
#define SIZE 10
int main() {

	double *in;
	klee_make_symbolic(&in, sizeof(in), "29e98722bd3c4557a93037a336d0c195");

	int n;
	klee_make_symbolic(&n, sizeof(n), "44f8b24f93314d3ab86f29d63ce3bcee");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int perm;
	klee_make_symbolic(&perm, sizeof(perm), "baa481bfd2e1455b895a22dc7d0568a0");
	if ((perm<-1) || (perm>1024)) {
		 return 0;}
	return det(in, n, perm);
}
