#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	charList *list;
	klee_make_symbolic(&list, sizeof(list), "d7d1ca3da1e4453b84146e8d3644caad");

	int index;
	klee_make_symbolic(&index, sizeof(index), "fce6c75bbcd945f38bed2f7cff5f275a");
	if ((index<-1) || (index>1024)) {
		 return 0;}
	return removeEl(list, index);
}
