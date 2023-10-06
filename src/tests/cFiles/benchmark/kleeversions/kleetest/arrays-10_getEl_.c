#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "e752513356cd490590677da50f42572d");

	int index;
	klee_make_symbolic(&index, sizeof(index), "bc5177c4ed10413da86493929a62ff5a");
	if ((index<-1) || (index>1024)) {
		 return 0;}
	return getEl(list, index);
}
