#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/14_lexicographic_array_compare.c>
#define SIZE 100
int main() {

	int x[SIZE];
	klee_make_symbolic(&x, sizeof(x), "2358552f43004a5d8dcdf42ab8c0dfd5");

	int y[SIZE];
	klee_make_symbolic(&y, sizeof(y), "9b19af902de14930a9e076f40c72d72b");

	int size;
	klee_make_symbolic(&size, sizeof(size), "17cb8555809c4ae0bad0f2298bf259e5");
	return compare_arrays(x, y, size);
}
