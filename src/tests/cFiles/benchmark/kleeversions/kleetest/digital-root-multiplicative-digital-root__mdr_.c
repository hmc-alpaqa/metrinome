#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/digital-root-multiplicative-digital-root.c>
#define SIZE 10
int main() {

	int *rmdr;
	klee_make_symbolic(&rmdr, sizeof(rmdr), "0678b10bf16342d08809ceec57f9c8f1");

	int *rmp;
	klee_make_symbolic(&rmp, sizeof(rmp), "b65a9c6dd14c4ca08ce7f6955dc56508");

	long long n;
	klee_make_symbolic(&n, sizeof(n), "fd79f77ec4cf47868a48dff96655c5ac");
	_mdr(rmdr, rmp, n);
	return 0;
}
