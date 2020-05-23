#include <klee/klee.h>
#include </app/code/tests/cFiles/merge_sort.c>
int main() {

	int arr[];
	klee_make_symbolic(&arr, sizeof(arr), "27ba0266d49e4500bdd73313ceb0ffff");

	int l;
	klee_make_symbolic(&l, sizeof(l), "1d41a2c565c340ed88f3b2c61fcce830");

	int r;
	klee_make_symbolic(&r, sizeof(r), "bddeafd45cb94a3cb19d0fb245298d8e");
	return mergeSort(arr, l, r);
}
