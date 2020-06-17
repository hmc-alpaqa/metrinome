#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/12_check_sorted_array.c>
#define SIZE 100
int main() {

	int array[SIZE];
	klee_make_symbolic(&array, sizeof(array), "0d491eb7709b4c5c96600bccc3551543");

	int size;
	klee_make_symbolic(&size, sizeof(size), "9b0a1e1149684044abfa6acf11e5a9d6");
	return is_sorted(array, size);
}
