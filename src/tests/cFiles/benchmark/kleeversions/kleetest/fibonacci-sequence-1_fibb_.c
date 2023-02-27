#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/fibonacci-sequence-1.c>
#define SIZE 10
int main() {

	long long a;
	klee_make_symbolic(&a, sizeof(a), "dea3c556bd20447ab139bf5293a0b013");

	long long b;
	klee_make_symbolic(&b, sizeof(b), "6eb2caf5b3d643f5b7187cdd743245af");

	int n;
	klee_make_symbolic(&n, sizeof(n), "b51cb2e0451943d7b2e526dc8c34a24b");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fibb(a, b, n);
}
