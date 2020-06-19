#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/23_mergesort.c>
#define SIZE 100
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "2e460ac5bc7841d9a6ab083e82ad755e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "b654eddd2e394e8ebb2961e95398c208");
	mergesort(arr, n);
	return 0;
}
