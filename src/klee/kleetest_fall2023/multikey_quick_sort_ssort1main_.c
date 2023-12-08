#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/multikey_quick_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	char x[SIZE][SIZE];
	klee_make_symbolic(&x, sizeof(x), "97ae68c925404d5ebcbe50d1eb4c2e96");

	int n;
	klee_make_symbolic(&n, sizeof(n), "53d0e554080946a6bb4a7a34320498e1");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	ssort1main(x, n);
	return 0;
}
