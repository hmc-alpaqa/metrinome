#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/cycle_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "2eadb1207eac4cb09429b68d8f35cf30");

	int n;
	klee_make_symbolic(&n, sizeof(n), "8e5ffcd1286d4bba882b8dae1c77e182");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	cycleSort(arr, n);
	return 0;
}
