#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/06_binarysearch_no_helper.c>
#define SIZE 10
int main() {

	int list[SIZE];
	klee_make_symbolic(&list, sizeof(list), "eff5e19b9d1e44c99c2c5af47b840d1e");

	int size;
	klee_make_symbolic(&size, sizeof(size), "1bc0bf6ede2a4b5e83ca0f6289787e2b");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	return mainn(list, size);
}
