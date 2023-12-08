#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/selection_sort_recursive.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int8_t arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "beabf82290a04d45aff4756f1ea52655");

	const uint8_t size;
	klee_make_symbolic(&size, sizeof(size), "4ec3537b9f444b2a9d67f73174b8900b");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	selectionSort(arr, size);
	return 0;
}
