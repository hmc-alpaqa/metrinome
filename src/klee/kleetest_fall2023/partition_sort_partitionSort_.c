#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/partition_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int arr[SIZE][SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "6ea91250b6a541b8bcb05076e32a63ea");

	int low;
	klee_make_symbolic(&low, sizeof(low), "5430b1da821f46d8b6c2d9279a89f070");
	if ((low<-1) || (low>1024)) {
		 return 0;}

	int high;
	klee_make_symbolic(&high, sizeof(high), "632ef16983954f37aa96ee9d5e111918");
	if ((high<-1) || (high>1024)) {
		 return 0;}
	partitionSort(arr, low, high);
	return 0;
}
