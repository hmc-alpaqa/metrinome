#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/50_check_sorted_or_reverse.c>
#define SIZE 100
int main() {

	int array[SIZE];
	klee_make_symbolic(&array, sizeof(array), "1e325fc675344745a812de0c5caee67c");

	int size;
	klee_make_symbolic(&size, sizeof(size), "424a4b71906d4306b598c04c498be7eb");
	return is_sorted_or_reverse(array, size);
}
