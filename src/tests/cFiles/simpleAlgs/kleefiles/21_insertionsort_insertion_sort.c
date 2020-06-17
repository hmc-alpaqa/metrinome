#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/21_insertionsort.c>
#define SIZE 100
int main() {

	int list[SIZE];
	klee_make_symbolic(&list, sizeof(list), "94e573873c3c4f4a8acc92c4367ba6a2");

	int count;
	klee_make_symbolic(&count, sizeof(count), "c4f69a33436044f68288fb326fb12a2f");
	return insertion_sort(list, count);
}
