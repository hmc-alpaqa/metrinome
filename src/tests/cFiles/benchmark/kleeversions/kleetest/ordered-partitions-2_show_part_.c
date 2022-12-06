#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ordered-partitions-2.c>
#define SIZE 10
int main() {

	uint x;
	klee_make_symbolic(&x, sizeof(x), "401cbe502723493cbd61b6a24a699b1b");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	show_part(x);
	return 0;
}
