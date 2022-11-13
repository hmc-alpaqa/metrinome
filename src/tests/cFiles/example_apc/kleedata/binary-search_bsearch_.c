#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/binary-search.c>
#define SIZE 10
int main() {

	int *a;
	klee_make_symbolic(&a, sizeof(a), "c14c0a66726f43bc9f995b7645b6dbeb");

	int n;
	klee_make_symbolic(&n, sizeof(n), "a2c9b0b742524b08874e8a01534a5f14");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "6500121cb107446392092d1b23b3a787");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return bsearch(a, n, x);
}
