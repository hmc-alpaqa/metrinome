#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/comb_sort.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int numbers[SIZE];
	klee_make_symbolic(&numbers, sizeof(numbers), "08abad9b760b4749a006f4b0b4e65a35");

	int size;
	klee_make_symbolic(&size, sizeof(size), "fce715fd18474bf7b2e78d9cb12adb0c");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	sort(numbers, size);
	return 0;
}
