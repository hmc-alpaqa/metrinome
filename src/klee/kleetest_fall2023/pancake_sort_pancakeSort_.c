#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/pancake_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "eafd430e59424ecea1b8dcd9ad10bc07");

	int n;
	klee_make_symbolic(&n, sizeof(n), "7017f65e58564000bec9b7e4068a6cce");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	pancakeSort(arr, n);
	return 0;
}
