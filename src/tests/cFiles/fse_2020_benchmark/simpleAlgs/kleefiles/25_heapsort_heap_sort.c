#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/25_heapsort.c>
#define SIZE 100
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "14cb3ac378654b0aa731c56f49d077b2");

	unsigned int len;
	klee_make_symbolic(&len, sizeof(len), "04e905efb62f4ab8840e40a9a51d2998");
	heap_sort(a, len);
	return 0;
}
