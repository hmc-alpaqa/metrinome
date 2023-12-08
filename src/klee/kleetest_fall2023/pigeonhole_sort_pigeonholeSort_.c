#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/pigeonhole_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "36cf93e7b6e94e088c8fc5b3299988ba");

	int size;
	klee_make_symbolic(&size, sizeof(size), "7c65af260b9d45b997e164ad041b43a8");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	pigeonholeSort(arr, size);
	return 0;
}
