#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/16_binary_search.c>
#define SIZE 100
int main() {

	int search;
	klee_make_symbolic(&search, sizeof(search), "f738de48181b4143926c8e1144bf9204");

	int array[SIZE];
	klee_make_symbolic(&array, sizeof(array), "cc0058e283704ca88e6c78892975e76d");

	int n;
	klee_make_symbolic(&n, sizeof(n), "67ed7557050d4058922948fdd28e0211");
	return binary_search(search, array, n);
}
