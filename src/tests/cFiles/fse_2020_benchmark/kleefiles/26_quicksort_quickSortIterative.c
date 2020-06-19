#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/26_quicksort.c>
#define SIZE 100
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "46771e438320461ba6607afd3921bace");

	int l;
	klee_make_symbolic(&l, sizeof(l), "b688fd2532d44a0e8c7b5cb38cf588d2");

	int h;
	klee_make_symbolic(&h, sizeof(h), "73b35d32bd7048358a73c68436238556");
	quickSortIterative(arr, l, h);
	return 0;
}
