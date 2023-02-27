#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/binary-search.c>
#define SIZE 10
int main() {

	int *a;
	klee_make_symbolic(&a, sizeof(a), "be646a1e722a4bdebd1b1a615c78bda0");

	int n;
	klee_make_symbolic(&n, sizeof(n), "1c05d27e4d6341fe85e163ba2de4da55");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "4f7f45ac5ba845b1aa62e3a478022647");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return bsearch(a, n, x);
}
