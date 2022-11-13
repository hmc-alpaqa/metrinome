#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "fdbffbfa96104ccd895e4c4e59c0ad6e");

	int index;
	klee_make_symbolic(&index, sizeof(index), "c6f5abc4f76740239373e8cc664124f3");
	if ((index<-1) || (index>1024)) {
		 return 0;}
	return getEl(list, index);
}
