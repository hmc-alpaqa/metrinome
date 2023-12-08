#include <klee/klee.h>
#include </app/code/tests/cFiles/C-master/searching/floyd_cycle_detection_algorithm.c>
#define SIZE 1024
#define MAX_VALUE 65536
int main() {

	const uint32_t in_arr[SIZE];
	klee_make_symbolic(&in_arr, sizeof(in_arr), "275b4f6b39444ff79c032425b61e4366");

	size_t n;
	klee_make_symbolic(&n, sizeof(n), "114638aa1f0f40a1988425033302a2d2");
	if ((n<=0) || (n>1024)) {
		 return 0;}
	return duplicateNumber(in_arr, n);
}
