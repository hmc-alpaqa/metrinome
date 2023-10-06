#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/binary-search.c>
#define SIZE 10
int main() {

	int *a;
	klee_make_symbolic(&a, sizeof(a), "6da8a5c384334d7ca9b235ddffc3f03f");

	int x;
	klee_make_symbolic(&x, sizeof(x), "216109dc6e3c44479b853e5b8ae0859d");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int i;
	klee_make_symbolic(&i, sizeof(i), "04af3805bc9c426792f40550c643fdd3");
	if ((i<-1) || (i>1024)) {
		 return 0;}

	int j;
	klee_make_symbolic(&j, sizeof(j), "7e14d137a8724ed8a692225809366089");
	if ((j<-1) || (j>1024)) {
		 return 0;}
	return bsearch_r(a, x, i, j);
}
