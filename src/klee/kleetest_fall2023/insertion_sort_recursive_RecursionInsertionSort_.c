#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/insertion_sort_recursive.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "ddc4f8265dc94d6693c01c3a0e3caf81");

	int size;
	klee_make_symbolic(&size, sizeof(size), "4a884157ca0945e89f6d816088ecfbb0");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	RecursionInsertionSort(arr, size);
	return 0;
}
