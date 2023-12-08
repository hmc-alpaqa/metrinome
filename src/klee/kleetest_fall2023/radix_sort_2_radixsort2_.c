#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/radix_sort_2.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "c64753efbc07472aa3498c72a0766f55");

	int n;
	klee_make_symbolic(&n, sizeof(n), "89e3c9fbc19c44b299d784cce70bfa35");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int max;
	klee_make_symbolic(&max, sizeof(max), "92480a242e714adab1463a4a5f8486de");
	if ((max<-1) || (max>1024)) {
		 return 0;}
	radixsort2(arr, n, max);
	return 0;
}
