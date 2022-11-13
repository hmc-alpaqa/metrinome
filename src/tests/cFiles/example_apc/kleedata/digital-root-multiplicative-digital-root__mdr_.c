#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/digital-root-multiplicative-digital-root.c>
#define SIZE 10
int main() {

	int *rmdr;
	klee_make_symbolic(&rmdr, sizeof(rmdr), "45df803685df4d3dbc80acc8904c8985");

	int *rmp;
	klee_make_symbolic(&rmp, sizeof(rmp), "8456d076c821487c829ed8eddca02379");

	long long n;
	klee_make_symbolic(&n, sizeof(n), "b8da209ef29a43b1aacb59c2d18665df");
	_mdr(rmdr, rmp, n);
	return 0;
}
