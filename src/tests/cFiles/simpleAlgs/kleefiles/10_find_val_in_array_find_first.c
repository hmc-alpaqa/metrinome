#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/10_find_val_in_array.c>
#define SIZE 100
int main() {

	int val;
	klee_make_symbolic(&val, sizeof(val), "4641dcdecbf14b0293cc7d8b63ae5209");

	int array[SIZE];
	klee_make_symbolic(&array, sizeof(array), "c381f290ef7749a3b0885f86171c89ce");

	int size;
	klee_make_symbolic(&size, sizeof(size), "0859805b00194297be823216c70818b9");
	return find_first(val, array, size);
}
