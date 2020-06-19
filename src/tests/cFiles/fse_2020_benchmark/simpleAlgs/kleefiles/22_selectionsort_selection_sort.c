#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/22_selectionsort.c>
#define SIZE 100
int main() {

	int list[SIZE];
	klee_make_symbolic(&list, sizeof(list), "9bfe3a11341646949eb2cc719b86e0f2");

	int count;
	klee_make_symbolic(&count, sizeof(count), "cb3647016eb048209e927f7a9b57a46e");
	selection_sort(list, count);
	return 0;
}
