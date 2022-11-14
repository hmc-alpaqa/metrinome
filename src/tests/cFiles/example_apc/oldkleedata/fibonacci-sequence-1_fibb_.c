#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/fibonacci-sequence-1.c>
#define SIZE 10
int main() {

	long long a;
	klee_make_symbolic(&a, sizeof(a), "b3006290ba3f4904932ed906c0a93809");

	long long b;
	klee_make_symbolic(&b, sizeof(b), "6bb3d77404474238b134b4ee0e950500");

	int n;
	klee_make_symbolic(&n, sizeof(n), "1d30480c644c40d5974b11dc4372b960");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fibb(a, b, n);
}
