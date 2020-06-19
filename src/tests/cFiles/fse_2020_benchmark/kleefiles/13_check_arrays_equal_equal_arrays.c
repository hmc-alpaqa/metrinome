#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/13_check_arrays_equal.c>
#define SIZE 100
int main() {

	int x[SIZE];
	klee_make_symbolic(&x, sizeof(x), "8d0e8b0750034f83a1b312768a425758");

	int y[SIZE];
	klee_make_symbolic(&y, sizeof(y), "c303eb4645d747cfb6f5cf16b04890fd");

	int size;
	klee_make_symbolic(&size, sizeof(size), "b47c7b386dae418fa4dccc8c3f6e1ad8");
	return equal_arrays(x, y, size);
}
