#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/binary_insertion_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "f9fa2a0730c64c1cac8dd90190e76bab");

	int size;
	klee_make_symbolic(&size, sizeof(size), "6f8ac543ce9343f88b2c2411b2e24304");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	insertionSort(arr, size);
	return 0;
}
