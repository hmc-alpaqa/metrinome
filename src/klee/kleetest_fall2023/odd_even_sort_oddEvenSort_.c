#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/odd_even_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "77c482ec1820487c803957d87154d79c");

	int size;
	klee_make_symbolic(&size, sizeof(size), "411f7a1c4f99496f9555d0bbb32ac3c2");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	oddEvenSort(arr, size);
	return 0;
}
