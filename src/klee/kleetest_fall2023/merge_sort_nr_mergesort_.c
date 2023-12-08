#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/merge_sort_nr.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int x[SIZE][SIZE];
	klee_make_symbolic(&x, sizeof(x), "177880259baf485fa966fc4430c1e935");

	int n;
	klee_make_symbolic(&n, sizeof(n), "5af30a57fdd6461f9f4508b434de88e4");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	mergesort(x, n);
	return 0;
}
