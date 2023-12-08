#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/selection_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "f6c54a0c23034ecfa8ee059641e87da4");

	int size;
	klee_make_symbolic(&size, sizeof(size), "d76217699cbc48a48d210347e3106c24");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	selectionSort(arr, size);
	return 0;
}
