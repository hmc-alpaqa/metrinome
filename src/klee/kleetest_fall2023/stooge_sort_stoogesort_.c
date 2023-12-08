#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/stooge_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "5b7363b672504eccb507e062b1557d5d");

	int i;
	klee_make_symbolic(&i, sizeof(i), "66710d8b500344f3918e833f6539171e");
	if ((i<-1) || (i>1024)) {
		 return 0;}

	int j;
	klee_make_symbolic(&j, sizeof(j), "ddba66bf503c4587880b546d8831507b");
	if ((j<-1) || (j>1024)) {
		 return 0;}
	stoogesort(arr, i, j);
	return 0;
}
