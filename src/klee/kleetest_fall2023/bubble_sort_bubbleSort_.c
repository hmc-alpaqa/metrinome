#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/bubble_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "059f08efc8104b6b9b908092b748c05e");

	int size;
	klee_make_symbolic(&size, sizeof(size), "53853181dae7475780a8a86c280e8c69");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	bubbleSort(arr, size);
	return 0;
}
