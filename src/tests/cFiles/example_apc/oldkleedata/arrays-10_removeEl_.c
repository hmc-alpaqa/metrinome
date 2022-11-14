#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "2b33f558420544b39151aaf3a2d5c332");

	int index;
	klee_make_symbolic(&index, sizeof(index), "baf1d7737a854c85956972807752fb1a");
	if ((index<-1) || (index>1024)) {
		 return 0;}
	return removeEl(list, index);
}
