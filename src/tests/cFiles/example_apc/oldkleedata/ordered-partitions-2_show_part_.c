#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ordered-partitions-2.c>
#define SIZE 10
int main() {

	uint x;
	klee_make_symbolic(&x, sizeof(x), "67832658cd2e4aa0b7ee108bc68e490f");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	show_part(x);
	return 0;
}
