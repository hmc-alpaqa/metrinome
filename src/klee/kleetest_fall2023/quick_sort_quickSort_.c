#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/quick_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "e9930653c38d4787b6edf093f8f5bfbe");

	int lower;
	klee_make_symbolic(&lower, sizeof(lower), "602a9cdd04324f4aa6a4b46f7a735ff7");
	if ((lower<-1) || (lower>1024)) {
		 return 0;}

	int upper;
	klee_make_symbolic(&upper, sizeof(upper), "3090300f5ffd426cb401cc2a8bfe67a8");
	if ((upper<-1) || (upper>1024)) {
		 return 0;}
	quickSort(arr, lower, upper);
	return 0;
}
