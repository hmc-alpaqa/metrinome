#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/insertion_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "690bf1a00e014709832baabdd6de33dd");

	int size;
	klee_make_symbolic(&size, sizeof(size), "621e9d4e1a924b6cb3e301f43f63bef1");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	insertionSort(arr, size);
	return 0;
}
