#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/06_binarysearch_no_helper.c>
#define SIZE 10
int main() {

	int list[SIZE];
	klee_make_symbolic(&list, sizeof(list), "81a5fd7d98b744c9863a10c7118f5b91");

	int size;
	klee_make_symbolic(&size, sizeof(size), "176e3100a2654ed89b00ef86bf888fd6");
	if ((size<-1) || (size>1024)) {
		 return 0;}
	return mainn(list, size);
}
