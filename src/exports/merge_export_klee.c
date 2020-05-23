#include <klee/klee.h>
#include </app/code/tests/cFiles/merge_sort.c>
#define SIZE 10
int main() {

	int arr[SIZE];
	klee_make_symbolic(&arr, sizeof(arr), "04bb4f7f6b144977b117970f9555f2dd");

	int l;
	klee_make_symbolic(&l, sizeof(l), "33a71e3ce1314bf281a1285f534bca2e");

	int m;
	klee_make_symbolic(&m, sizeof(m), "3b925e1792c5445fb8f7b5141c2e5011");

	int r;
	klee_make_symbolic(&r, sizeof(r), "cc90bc0b7e8042cc83312e2daf24ed42");
	merge(arr, l, m, r);
	return 0;
}
