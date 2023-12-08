#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/sorting/shell_sort2.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	int array[SIZE];
	klee_make_symbolic(&array, sizeof(array), "7df764e802cd4446b68c1495ae644831");

	long LEN;
	klee_make_symbolic(&LEN, sizeof(LEN), "5f7c5d12d41c44ebaf6d185f5b1c148e");
	shell_sort(array, LEN);
	return 0;
}
